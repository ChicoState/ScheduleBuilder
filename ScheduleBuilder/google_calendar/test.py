from google_calendar.views import *
from account.views import *
from django.urls import reverse
from django.test import Client
from unittest.mock import Mock, patch
import requests
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

# Summary, 6 test cases for get_recurrence_rule

def test_get_recurrence_rule_weekly():
    option = 'weekly'
    due_date = '2024-01-01'
    actual = get_recurrence_rule(option, due_date)
    expected = 'FREQ=WEEKLY;UNTIL=20240101T000000Z'
    assert actual == expected

def test_get_recurrence_rule_daily():
    option = 'daily'
    due_date = '2024-01-01'
    actual = get_recurrence_rule(option, due_date)
    expected = 'FREQ=DAILY;UNTIL=20240101T000000Z'
    assert actual == expected

def test_get_recurrence_rule_monthly():
    option = 'monthly'
    due_date = '2024-01-01'
    actual = get_recurrence_rule(option, due_date)
    expected = 'FREQ=MONTHLY;UNTIL=20240101T000000Z'
    assert actual == expected

def test_get_recurrence_rule_yearly():
    option = 'yearly'
    due_date = '2024-01-01'
    actual = get_recurrence_rule(option, due_date)
    expected = 'FREQ=YEARLY;UNTIL=20240101T000000Z'
    assert actual == expected

def test_get_recurrence_rule_invalid_option():
    option = 'invalid'
    due_date = '2024-01-01'
    actual = get_recurrence_rule(option, due_date)
    expected = ''
    assert actual == expected

def test_get_recurrence_rule_invalid_date():
    option = 'weekly'
    invalid_due_date = 'invalid_date'
    try:
        actual = get_recurrence_rule(option, invalid_due_date)
        assert False, "Expected ValueError, but function returned: {}".format(actual)
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

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_testICAL(driver):
    driver.get("http://127.0.0.1:8000/")
    driver.set_window_size(1212, 804)
    driver.find_element(By.LINK_TEXT, "Icalendar Upload").click()
    driver.find_element(By.ID, "ical_url").click()
    driver.find_element(By.ID, "ical_url").send_keys("https://canvas.csuchico.edu/feeds/calendars/user_R4cNve0gRKZuiCFpRDx9eyLSbtNLguIA3C8brXSH.ics")
    driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    driver.find_element(By.LINK_TEXT, "Edit").click()
    driver.find_element(By.ID, "id_due_date").click()
    driver.find_element(By.ID, "id_due_date").send_keys("2023-12-12")
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > td").click()
    driver.find_element(By.ID, "id_event_name").send_keys("ex class")
    driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td").click()
    driver.find_element(By.ID, "id_start_date").click()
    driver.find_element(By.ID, "id_start_date").send_keys("2023-12-12")
    driver.find_element(By.ID, "id_time_to_spend").click()
    driver.find_element(By.ID, "id_time_to_spend").send_keys("0")
    driver.find_element(By.ID, "id_priority_1").click()
    driver.find_element(By.ID, "id_progress_2").click()
    driver.find_element(By.ID, "id_amount_per_week").click()
    driver.find_element(By.ID, "id_amount_per_week").send_keys("1")
    driver.find_element(By.NAME, "add").click()
    assert "EVENT CREATED" in driver.page_source
  


