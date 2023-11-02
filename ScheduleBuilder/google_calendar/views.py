from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from google_calendar.forms import EventForm, SubmitType, CalendarForm

from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery

# constants for connecting to google calendar API
CAL_ID = config('CAL_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './core/calendar-credentials.json'

# view for localhost/calendar/
@login_required(login_url='/login/')
def main(request):
    results = []
    context = {"results": results}
    return render(request, 'calendar/calendar.html', context)

@login_required(login_url='/login/')
def create_calendar(request):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    if request.method == 'POST':
        if 'add' in request.POST:
            # form to add event
            add_form = CalendarForm(request.POST)
            if add_form.is_valid():
                calendar = add_form.save(commit=False)
                calendar.save()
                name = add_form.cleaned_data['name']
                calendar_attrs = {
                        'summary': name
                }
                response = service.calendars().insert(body=calendar_attrs).execute()
                print(response)
                return redirect('/calendar/')
                # if add form isnt valid
            else:
                context = {
                    'form_data': add_form
                }
                return render(request, 'calendar/create_calendar.html', context)
        else: 
            # canceled
            return redirect('/calendar/')
    else:
        context = {
            'form_data' : CalendarForm()
        }
        return render(request, 'calendar/create_calendar.html', context)

    return HttpResponse("Create Calendar Page")

# View for localhost/calendar/add/
@login_required(login_url='/login/')
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
                assigned_date = add_form.cleaned_data['assigned_date'].isoformat()
                due_date = add_form.cleaned_data['due_date'].isoformat()
                # CREATE A NEW EVENT IN CALENDAR
                new_event = {
                'summary': add_form.cleaned_data['assignment_name'],
                'location': f'{add_form.cleaned_data["class_name"]}',
                'description': 'Assignment',
                'start': {
                    'date': f'{assigned_date}',
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'date': f"{due_date}",
                    'timeZone': 'America/Los_Angeles',
                },
                }
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
