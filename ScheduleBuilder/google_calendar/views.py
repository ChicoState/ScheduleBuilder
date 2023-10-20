from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from google_calendar.forms import EventForm, SubmitType

from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery

from icalendar import Calendar
import requests

# constants for connecting to google calendar API
CAL_ID = config('CAL_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './core/calendar-credentials.json'

# view for localhost/calendar/
def calendar(request):
    # Your existing calendar view logic here
    results = []
    context = {"results": results}
    return render(request, 'calendar/calendar.html', context)

def icalendar(request):
    ical_url = request.session.get('ical_url')
    ical_events = request.session.get('ical_events', [])
    form = None

    if ical_url and ical_events:
        ical_event = ical_events[0]
        initial_data = {
            'event_name': ical_event['summary'],
            'class_name': '',
            'assigned_date': ical_event['start'],
            'due_date': ical_event['end'],
        }
        form = EventForm(request.POST or None, initial=initial_data)

        if request.method == 'POST':
            if 'add' in request.POST:
                if form.is_valid():
                    event = form.save(commit=False)
                    event.save()
                    ical_events.pop(0)

                    if ical_events:
                        next_ical_event = ical_events[0]
                        initial_data = {
                            'event_name': next_ical_event['summary'],
                            'class_name': '',
                            'assigned_date': next_ical_event['start'],
                            'due_date': next_ical_event['end'],
                        }
                        form = EventForm(initial=initial_data)
                    else:
                        # All events are added, clear the session variable and redirect to the calendar
                        request.session.pop('ical_events', None)
                        return redirect('/calendar/')

    context = {
        "form_data": form
    }

    return render(request, 'calendar/add_assignment.html', context)

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
                event_description = f'Priority: {event.priority}\nProgress: {event.progress}\nTime to Spend: {event.time_to_spend}\nAmount per Week: {event.amount_per_week}'
                # CREATE A NEW EVENT IN CALENDAR
                new_event = {
                'summary': add_form.cleaned_data['event_name'],
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
                if add_form.cleaned_data['class_name']:
                    new_event['location'] = f'{add_form.cleaned_data["class_name"]}'
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
        context = {
            'form_data' : EventForm()
        }
        return render(request, 'calendar/add_assignment.html', context)
    
