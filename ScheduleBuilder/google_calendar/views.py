from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from google_calendar.calendar_API import test_calendar
from google_calendar.forms import EventForm
def main(request):
    results = test_calendar()
    context = {"results": results}
    return render(request, 'calendar/calendar.html', context)


def add(request):
    if request.method == 'POST':
        add_form = EventForm(request.POST)
        if add_form.is_valid():
            pass
    return render(request, 'calendar/add_assignment.html')
