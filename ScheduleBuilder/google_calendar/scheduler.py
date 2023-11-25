from datetime import datetime, timedelta
from google.oauth2 import service_account
import googleapiclient.discovery
from decouple import config

CAL_ID = config('CAL_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './core/calendar-credentials.json'

def get_user_busy_times():
    # Implement this function to fetch the user's busy times from Google Calendar
    # You can use the Google Calendar API to retrieve the user's events
    # and extract busy times from those events.
    # Return a list of busy time ranges (start_time, end_time).

    # Example: Dummy data for testing
    busy_times = [
        (datetime.now(), datetime.now() + timedelta(hours=1)),
        (datetime.now() + timedelta(hours=2), datetime.now() + timedelta(hours=4)),
    ]

    return busy_times

def schedule_assignments(assignments, busy_times):
    # Implement this function to schedule assignments while avoiding busy times.
    # Return a list of scheduled assignments with start_time and end_time.

    scheduled_assignments = []

    # Example: Dummy scheduling algorithm (sort assignments by priority and schedule sequentially)
    assignments.sort(key=lambda x: x.priority, reverse=True)

    for assignment in assignments:
        # Dummy logic: Schedule assignment for 1 hour
        start_time = datetime.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)

        # Check if the scheduled time overlaps with busy times
        overlap = any(
            start < end_time and end > start_time for start, end in busy_times
        )

        if not overlap:
            scheduled_assignments.append({
                'assignment': assignment,
                'start_time': start_time,
                'end_time': end_time,
            })

    return scheduled_assignments

def add_assignments_to_calendar(scheduled_assignments):
    # Implement this function to add scheduled assignments to Google Calendar.
    # Use the Google Calendar API to create events for each scheduled assignment.

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=credentials
    )

    for scheduled_assignment in scheduled_assignments:
        assignment = scheduled_assignment['assignment']
        start_time = scheduled_assignment['start_time'].isoformat()
        end_time = scheduled_assignment['end_time'].isoformat()

        event_description = f'Priority: {assignment.priority}\nProgress: {assignment.progress}\nTime to Spend: {assignment.time_to_spend}\nAmount per Week: {assignment.amount_per_week}'

        new_event = {
            'summary': assignment.event_name,
            'location': assignment.class_name,
            'description': event_description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Los_Angeles',
            },
        }

        # Add event to calendar
        service.events().insert(calendarId=CAL_ID, body=new_event).execute()
        print(f'EVENT CREATED for {assignment.event_name}')
