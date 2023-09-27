from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from google_calendar.calendar_API import test_calendar
from google_calendar.forms import EventForm, SubmitType

from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery
import datetime

CAL_ID = config('CAL_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './core/calendar-credentials.json'

def main(request):
    # if SubmitType.objects.count() == 0:
        
    # results = test_calendar()
    results = []
    
    context = {"results": results}
    return render(request, 'calendar/calendar.html', context)


def add(request):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    if request.method == 'POST':
        if 'add' in request.POST:
            add_form = EventForm(request.POST)
            if add_form.is_valid():
                event = add_form.save(commit=False)
                event.save()
                
                print(type(add_form.cleaned_data['assigned_date']))
                print(type(add_form.cleaned_data['due_date']))
                assigned_date = add_form.cleaned_data['assigned_date'].isoformat()
                print(f"ASSIGNED DATE: {assigned_date}")
                due_date = add_form.cleaned_data['due_date'].isoformat()
                print(f"DUE DATE: {due_date}")
                # datetime.combine(add_form.cleaned_data["assigned_date"], datetime.min.time())
                
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
                ####################
                # new_event = {
                #     'summary': add_form.cleaned_data['assignment_name'],
                #     'location': add_form.cleaned_data['class_name'],
                #     # 'description': add_form.cleaned_data['submission_type'],
                #     'start': {
                #         'date': f'{assigned_date}',
                #         'timeZone': 'America/Los_Angeles'
                #     },
                #     'end': {
                #         'date': f'{due_date}',
                #         'timeZone': 'America/Los_Angeles'
                #     },
                # }
                ######################
                service.events().insert(calendarId=CAL_ID, body=new_event).execute()
                print('EVENT CREATED')
                return redirect('/calendar/')
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
