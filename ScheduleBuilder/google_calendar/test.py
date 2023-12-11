import time
import requests
import pytest
from google_calendar.views import *
from profile.views import *
from django.urls import reverse
from django.test import Client
from unittest.mock import Mock, patch
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

# 1 test case to register an account so other tests work

def test_addtestinguser(driver):
    try:
        driver.get("http://127.0.0.1:8000/login/?next=/")
        driver.set_window_size(1212, 804)
        driver.find_element(By.LINK_TEXT, "Register").click()
        driver.find_element(By.ID, "id_email").send_keys("tashelton@csuchico.edu")
        driver.find_element(By.ID, "id_username").click()
        driver.find_element(By.ID, "id_username").send_keys("12")
        driver.find_element(By.ID, "id_password1").click()
        driver.find_element(By.ID, "id_password1").send_keys("12")
        driver.find_element(By.ID, "id_password2").click()
        driver.find_element(By.ID, "id_password2").send_keys("12")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    except Exception as e:
        print("ERROR test failed")
        raise

# one test case to ensure icalendar works properly
# NOTE: must scroll when you reach to add form or test will fail

def test_testICAL(driver):
    try:
        driver.get("http://127.0.0.1:8000/")
        driver.set_window_size(1212, 1212)
        driver.find_element(By.ID, "id_username").send_keys("tashelton@csuchico.edu")
        driver.find_element(By.ID, "id_password").click()
        driver.find_element(By.ID, "id_password").send_keys("12")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        driver.find_element(By.LINK_TEXT, "Icalendar Upload").click()
        driver.find_element(By.ID, "ical_url").click()
        driver.find_element(By.ID, "ical_url").send_keys("https://canvas.csuchico.edu/feeds/calendars/user_R4cNve0gRKZuiCFpRDx9eyLSbtNLguIA3C8brXSH.ics")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        driver.find_element(By.LINK_TEXT, "Edit").click()
        driver.find_element(By.ID, "id_due_date").click()
        driver.find_element(By.ID, "id_due_date").clear()
        driver.find_element(By.ID, "id_due_date").send_keys("2024-01-01")
        driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > td").click()
        driver.find_element(By.ID, "id_event_name").clear()
        driver.find_element(By.ID, "id_event_name").send_keys("ex class")
        driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td").click()
        driver.find_element(By.ID, "id_start_date").click()
        driver.find_element(By.ID, "id_start_date").clear()
        driver.find_element(By.ID, "id_start_date").send_keys("2024-01-01")
        driver.find_element(By.ID, "id_class_name").click()
        driver.find_element(By.ID, "id_class_name").clear()
        driver.find_element(By.ID, "id_time_to_spend").click()
        driver.find_element(By.ID, "id_time_to_spend").send_keys("0")
        driver.find_element(By.ID, "id_priority_1").click()
        driver.find_element(By.ID, "id_progress_2").click()
        time.sleep(5)
        driver.find_element(By.ID, "id_amount_per_week").click()
        driver.find_element(By.ID, "id_amount_per_week").send_keys("1")
        driver.find_element(By.NAME, "add").click()
        driver.find_element(By.LINK_TEXT, "Delete Assignment").click()
        driver.find_element(By.ID, "event-title-input").click()
        driver.find_element(By.ID, "event-title-input").send_keys("ex class")
        driver.find_element(By.ID, "due-date-input").click()
        driver.find_element(By.ID, "due-date-input").send_keys("2024-01-01")
        driver.find_element(By.ID, "start-date-input").click()
        driver.find_element(By.ID, "start-date-input").send_keys("2024-01-01")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    except Exception:
        print("ERROR test failed must scroll when at forms to add event on sleep line")
        raise

# 1 test to sending friend requests 
# NOTE: must have one friend added or test will fail

def test_addFriendRemoveFriend(driver):
    try:
        driver.get("http://127.0.0.1:8000/")
        driver.set_window_size(1212, 804)
        driver.find_element(By.ID, "id_username").send_keys("tashelton@csuchico.edu")
        driver.find_element(By.ID, "id_password").click()
        driver.find_element(By.ID, "id_password").send_keys("12")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        driver.find_element(By.LINK_TEXT, "Account").click()
        driver.find_element(By.CSS_SELECTOR, ".friend-text").click()
        driver.find_element(By.CSS_SELECTOR, ".card:nth-child(1) > .card-center .card-title").click()
        driver.find_element(By.LINK_TEXT, "Unfriend").click()
        assert "Successfully removed that friend." in driver.page_source
        driver.find_element(By.ID, "id_send_friend_request_btn").click()
        assert "Friend request sent." in driver.page_source
    except Exception:
        print("ERROR test failed - Check that you have one friend")
        raise
  
# 1 test to ensure user can add an event, edit it, and delete it
# NOTE: must scroll when you reach to add form or test will fail

def test_eventtest(driver):
    try:
        driver.get("http://127.0.0.1:8000/")
        driver.set_window_size(1212, 850)
        driver.find_element(By.ID, "id_username").send_keys("tashelton@csuchico.edu")
        driver.find_element(By.ID, "id_password").click()
        driver.find_element(By.ID, "id_password").send_keys("12")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        driver.find_element(By.LINK_TEXT, "Calendar").click()
        driver.find_element(By.LINK_TEXT, "Add Assignment").click()
        driver.find_element(By.ID, "id_event_name").click()
        driver.find_element(By.ID, "id_event_name").send_keys("test sel")
        driver.find_element(By.ID, "id_start_date").click()
        driver.find_element(By.ID, "id_start_date").send_keys("2024-01-01")
        driver.find_element(By.ID, "id_due_date").click()
        driver.find_element(By.ID, "id_due_date").send_keys("2024-01-01")
        driver.find_element(By.ID, "id_time_to_spend").click()
        driver.find_element(By.ID, "id_time_to_spend").send_keys("0")
        driver.find_element(By.ID, "id_priority_0").click()
        driver.find_element(By.ID, "id_progress_2").click()
        time.sleep(5)
        driver.find_element(By.ID, "id_amount_per_week").click()
        driver.find_element(By.ID, "id_amount_per_week").send_keys("1")
        driver.find_element(By.NAME, "add").click()
        driver.find_element(By.LINK_TEXT, "Edit Assignment").click()
        driver.find_element(By.ID, "event-title-input").click()
        driver.find_element(By.ID, "event-title-input").send_keys("test sel")
        driver.find_element(By.ID, "due-date-input").click()
        driver.find_element(By.ID, "due-date-input").send_keys("2024-01-01")
        driver.find_element(By.ID, "start-date-input").click()
        driver.find_element(By.ID, "start-date-input").send_keys("2024-01-01")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        driver.find_element(By.ID, "id_time_to_spend").click()
        driver.find_element(By.ID, "id_time_to_spend").send_keys("1")
        driver.find_element(By.NAME, "edit").click()
        driver.find_element(By.LINK_TEXT, "Delete Assignment").click()
        driver.find_element(By.ID, "event-title-input").click()
        driver.find_element(By.ID, "event-title-input").send_keys("test sel")
        driver.find_element(By.ID, "due-date-input").click()
        driver.find_element(By.ID, "due-date-input").send_keys("2024-01-01")
        driver.find_element(By.ID, "start-date-input").click()
        driver.find_element(By.ID, "start-date-input").send_keys("2024-01-01")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    except Exception:
        print("ERROR test failed - must scroll when at forms to add event on sleep line")
        raise

  


