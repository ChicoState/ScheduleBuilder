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
        
    results = test_calendar()
    # results = []
    context = {"results": results}
    return render(request, 'calendar/calendar.html', context)


def add(request):
    if request.method == 'POST':
        if 'add' in request.POST:
            add_form = EventForm(request.POST)
            if add_form.is_valid():
                event = add_form.save(commit=False)
                event.save()
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
