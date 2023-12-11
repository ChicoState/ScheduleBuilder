from google_calendar.views import *
from profile.views import *
from django.urls import reverse
from django.test import Client
from unittest.mock import Mock, patch
import requests
import pytest

# Summary, 6 test cases for get_recurrence_rule

def test_get_recurrence_rule_weekly():
    option = 'weekly'
    due_date = '2023-12-31'
    result = get_recurrence_rule(option, due_date)
    expected = 'FREQ=WEEKLY;UNTIL=20231231T000000Z'
    assert result == expected

def test_get_recurrence_rule_daily():
    option = 'daily'
    due_date = '2023-12-31'
    result = get_recurrence_rule(option, due_date)
    expected = 'FREQ=DAILY;UNTIL=20231231T000000Z'
    assert result == expected

def test_get_recurrence_rule_monthly():
    option = 'monthly'
    due_date = '2023-12-31'
    result = get_recurrence_rule(option, due_date)
    expected = 'FREQ=MONTHLY;UNTIL=20231231T000000Z'
    assert result == expected

def test_get_recurrence_rule_yearly():
    option = 'yearly'
    due_date = '2023-12-31'
    result = get_recurrence_rule(option, due_date)
    expected = 'FREQ=YEARLY;UNTIL=20231231T000000Z'
    assert result == expected

def test_get_recurrence_rule_invalid_option():
    option = 'invalid'
    due_date = '2023-12-31'
    result = get_recurrence_rule(option, due_date)
    expected = ''
    assert result == expected

def test_get_recurrence_rule_invalid_date():
    option = 'weekly'
    invalid_due_date = 'invalid_date'
    try:
        result = get_recurrence_rule(option, invalid_due_date)
        assert False, "Expected ValueError, but function returned: {}".format(result)
    except ValueError:
        pass

def test_successful_icalendar_fetch_and_parsing():
    client = Client()
    ical_url = 'https://canvas.csuchico.edu/feeds/calendars/user_R4cNve0gRKZuiCFpRDx9eyLSbtNLguIA3C8brXSH.ics'
    response = requests.get(ical_url)
    ical_content = response.text
    response_mock = Mock(status_code=200, text=ical_content)
    with patch('requests.get', return_value=response_mock):
        response = client.post(reverse('icalendar-add'), {'ical_url': ical_url})
    assert response.status_code == 200
    assert 'event_name' in response.content.decode('utf-8')
    assert 'class_name' in response.content.decode('utf-8')
    assert 'due_date' in response.content.decode('utf-8')

def test_failed_icalendar_fetch_invalid_url():
    client = Client()
    ical_url = 'invalid_url'
    response_mock = Mock(status_code=404, text='Not Found')
    with patch('requests.get', return_value=response_mock):
        response = client.post(reverse('icalendar-add'), {'ical_url': ical_url})
    assert response.status_code == 200
    assert 'results' in response.context
    assert response.context['results'] == []

def test_no_icalendar_url_provided():
    client = Client()
    response = client.post(reverse('icalendar-add'))
    print(response.context['results'])
    assert response.status_code == 200
    assert 'results' in response.context
    assert response.context['results'] == []

