# core/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from PyPDF2 import PdfReader
import os
import tempfile
from .assignment_parser import assignment_parser
from .ScheduleParser import parse_keywords, parse_tables, parse_schedule, extract_grade_breakdown
import pdfplumber
import re
import pandas as pd
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery
from datetime import datetime

# constants for connecting to google calendar API
CAL_ID = config('CAL_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'calendar-credentials.json'
file_path = os.path.join(os.path.dirname(__file__), SERVICE_ACCOUNT_FILE)

@login_required
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf = PdfReader(pdf_file)
    for page in pdf.pages:
        page_text = page.extract_text()
        # Remove excess whitespace and normalize the text
        page_text = ' '.join(page_text.split())
        text += page_text + "\n"
    return text

@login_required
def home(request):
    user = request.user  # Assuming the user is authenticated
    # Credentials to connect to google cloud API and service account to add events to calendar
    credentials = service_account.Credentials.from_service_account_file(file_path, scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    # Define parameters to fetch upcoming events
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
    not_started_assignments = []
    in_progress_assignments = []
    completed_assignments = []
    today_event_titles = []  # Initialize list for today's event titles
    for event in events:
        description = event.get('description', '')
        due_date = event.get('end', '')
        if due_date:
            due_date_string = due_date['date']
            due_date_date = datetime.strptime(due_date_string, '%Y-%m-%d')
            current_date = datetime.now().date()

            if due_date_date.date() == current_date:
                today_event_titles.append(event.get('summary', ''))
        if "Progress: not started" in description:
            not_started_assignments.append(event.get('summary', ''))
        elif "Progress: in progress" in description:
            in_progress_assignments.append(event.get('summary', ''))
        elif "Progress: completed" in description:
            completed_assignments.append(event.get('summary', ''))

         # Calculate the overall progress for assignments
    total_assignments = len(events)
    in_progress_count = len(in_progress_assignments)
    completed_count = len(completed_assignments)
    overall_progress = ((completed_count + (in_progress_count / 2)) / total_assignments) if total_assignments > 0 else 1.0

    return render(request, 'core/home.html', {
        'overall_progress': overall_progress,
        'not_started_assignments': not_started_assignments,
        'in_progress_assignments': in_progress_assignments,
        'completed_assignments': completed_assignments,
        'today_event_titles': today_event_titles, 
        'user_name': user.username})

def parser(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            option = form.cleaned_data['option']
            temp_file_path = None
            
            if uploaded_file and option == 'assignment':
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                        temp_file.write(extract_text_from_pdf(uploaded_file).encode('utf-8'))
                        temp_file_path = temp_file.name

                    parser = assignment_parser(temp_file_path, uploaded_file.name)
                    parser.process_assignment()
                    parsed_contents = parser.get_parsed_contents()

                    return render(request, 'core/assignment_result.html', {'parsed_contents': parsed_contents})
                finally:
                    if temp_file_path:
                        os.remove(temp_file_path)
            
                return render(request, 'core/assignment_result.html', {'parsed_contents': parsed_contents})

            elif uploaded_file and option == 'syllabus':
               # Extract tables from the uploaded PDF using PDFPlumber
               with pdfplumber.open(uploaded_file) as pdf:
                   tables_parsed = []
                   for page in pdf.pages:
                       for table in page.extract_tables():
                           if parse_tables(table):
                               tables_parsed.append(table)
               syllabus_contents = extract_text_from_pdf(uploaded_file) 
               text_schedule = parse_schedule(syllabus_contents)
               grade_breakdown = extract_grade_breakdown(syllabus_contents)
               course = re.findall(r"[A-Z][A-Za-z\s-]{1,5}\d{3}", syllabus_contents)
               if course:
                   course = course[0]
               keyword_occurrences = parse_keywords(syllabus_contents)
               return render(request, 'core/syllabus_result.html', {'Important_Syllabus_Info': syllabus_contents, 'Course': course,'keywords': keyword_occurrences, 'tables_parsed': tables_parsed, 'schedule': text_schedule, 'grade_breakdown': grade_breakdown})
    else:
        form = UploadFileForm()

    return render(request, 'parser/parser.html', {'form': form})



