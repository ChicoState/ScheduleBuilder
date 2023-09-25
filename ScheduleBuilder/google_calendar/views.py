from django.shortcuts import render, redirect
from django.http import HttpResponse
from google_calendar.calendar_API import test_calendar

def main(request):
    results = test_calendar()
    context = {"results": results}
    return render(request, 'calendar/calendar.html', context)


def add(request):
    return HttpResponse