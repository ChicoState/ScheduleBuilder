from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from google_calendar.forms import EventForm, SubmitType

from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery
from googleapiclient.errors import HttpError

from icalendar import Calendar
import requests
from datetime import datetime
import re

# constants for connecting to google calendar API
CAL_ID = config('CAL_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './core/calendar-credentials.json'

# view for localhost/calendar/


def calendar(request):
    results = []
    context = {"results": results}
    return render(request, 'calendar/calendar.html', context)


def icalendar(request):
    ical_url = request.POST.get('ical_url') 
    results = []

    if ical_url:
        # Fetch events from the iCalendar URL
        response = requests.get(ical_url)
        if response.status_code == 200:
            cal = Calendar.from_ical(response.text)
            for event in cal.walk('vevent'):
                summary = event.get('summary')
                split_result = summary.split('[')
                event_name = split_result[0]
                class_name = split_result[1]
                pattern = r'\d{4}-(\w+-\d+)'
                # Use the re.search function to find the pattern in the input string
                match = re.search(pattern, class_name)
                class_name = match.group(1)  # Extract the matched name part

                start = event.get('dtstart')
                if start is not None:
                    start = start.dt
                else:
                    start = 'N/A'
                results.append(
                    {'summary': event_name, 'class_name': class_name, 'start': start})
    return render(request, 'parser/icalendar.html', {'results': results})

def get_recurrence_rule(option, due_date):
    # Define a mapping of recurrence options to recurrence rules
    due_date_datetime = datetime.strptime(due_date, '%Y-%m-%d')
    due_date_iso = due_date_datetime.strftime('%Y%m%dT%H%M%SZ')
    recurrence_rules = {
        'weekly': f'FREQ=WEEKLY;UNTIL={due_date_iso}',
        'daily': f'FREQ=DAILY;UNTIL={due_date_iso}',
        'monthly': f'FREQ=MONTHLY;UNTIL={due_date_iso}',
        'yearly': f'FREQ=YEARLY;UNTIL={due_date_iso}',
    }

    recurrence_rule = recurrence_rules.get(option, '')
    return recurrence_rule


# View for localhost/calendar/add/
def add(request):
    # Credentials to connect to google cloud API and service account to add events to calendar
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    if request.method == 'POST':
        if 'add' in request.POST:
            # form to add event
            add_form = EventForm(request.POST)
            if add_form.is_valid():
                event = add_form.save(commit=False)
                event.save()
                # need to convert dates into ISO format for calendar events
                start_date = add_form.cleaned_data['start_date'].isoformat()
                due_date = add_form.cleaned_data['due_date'].isoformat()
                # Get the recurrence option from the form
                recurrence_option = add_form.cleaned_data.get('repeat')
                recurrence_date = add_form.cleaned_data.get('repeat_until')
                if recurrence_date:
                    recurrence_date = recurrence_date.isoformat()
                recurrence_rule = None

                if recurrence_option:
                    recurrence_rule = get_recurrence_rule(recurrence_option, recurrence_date)
                event_description = f'Priority: {event.priority}\nProgress: {event.progress}\nTime to Spend: {event.time_to_spend}\nAmount per Week: {event.amount_per_week}'
                # CREATE A NEW EVENT IN CALENDAR
                new_event = {
                'summary': add_form.cleaned_data['event_name'],
                'location': f'{add_form.cleaned_data["class_name"]}',
                'description': event_description,
                'start': {
                    'date': f'{start_date}',
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'date': f"{due_date}",
                    'timeZone': 'America/Los_Angeles',
                },
                }
                if recurrence_rule:
                    new_event['recurrence'] = [f'RRULE:{recurrence_rule}']

                # add event to calendar
                service.events().insert(calendarId=CAL_ID, body=new_event).execute()
                print('EVENT CREATED')
                return redirect('/calendar/')
            # if add form isnt valid
            else:
                context = {
                    'form_data': add_form
                }
                return render(request, 'calendar/add_assignment.html', context)
        else: 
            # canceled
            return redirect('/calendar/')
    else:
        # If it's not a POST request, retrieve data from GET parameters
        event_name = request.GET.get('event_name', '')
        class_name = request.GET.get('class_name', '')
        due_date = request.GET.get('due_date', '')
        form_data = EventForm(initial={'event_name': event_name, 'class_name': class_name, 'due_date': due_date})
        context = {
            'form_data' : form_data
        }
        return render(request, 'calendar/add_assignment.html', context)
    
def delete(request):
    event_title = request.GET.get('event_title')
    due_date = request.GET.get('due_date')
    due_date = datetime.strptime(due_date, '%Y-%m-%d')
    start_date = request.GET.get('start_date')
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    if request.method == 'GET':
        if 'event_title' in request.GET:
            calendar_id = CAL_ID  # Replace with your calendar ID
            now = datetime.utcnow()
            events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=now.isoformat() + 'Z',  # Filter events that start from now or later
            maxResults=10,  # Maximum number of events to retrieve
            singleEvents=True,
            orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
            for event in events:
                due_date_var = event.get('end', '')
                if due_date_var:
                    due_date_string = due_date_var['date']
                    due_date_date = datetime.strptime(due_date_string, '%Y-%m-%d')
                start_date_var = event.get('start', '')
                if start_date_var:
                    start_date_string = start_date_var['date']
                    start_date_date = datetime.strptime(start_date_string, '%Y-%m-%d')
                if event.get('summary', '') == event_title:
                    if due_date_date.date() == due_date.date() and start_date_date.date() == start_date.date():
                        print("EVENT DELETED")
                        event_id = event.get('id', '')
                        service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()
    context = {}
    return render(request, 'calendar/calendar.html', context)