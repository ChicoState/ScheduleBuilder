[![Django Build](https://github.com/ChicoState/ScheduleBuilder/actions/workflows/django.yml/badge.svg)](https://github.com/ChicoState/ScheduleBuilder/actions/workflows/django.yml)
[![Django Tests](https://github.com/ChicoState/ScheduleBuilder/actions/workflows/tests.yml/badge.svg)](https://github.com/ChicoState/ScheduleBuilder/actions/workflows/tests.yml)
[![Test Coverage](https://codecov.io/gh/jcdodson/ScheduleBuilder/graph/badge.svg?token=N166XGA3EI)](https://codecov.io/gh/jcdodson/ScheduleBuilder)
# ScheduleBuilder
A schedule building application developed using the Django framework. Designed to streamline the scheduling process, optimizing time allocation, whether for individual use or planning with friends.

## Installation

Python and Django need to be installed
```bash
pip install django
```

Install all needed modules
```bash
pip install -r requirements.txt
```

Set your CAL_ID <br>
Running locally
```bash
set CAL_ID=c_6ed17073345c64d5b392f5a8ef7b4a62938f12c8fc5fecfa4b7256ef88acad28@group.calendar.google.com
```
**OR**<br>
Running in virtual enviroment
```bash
$env:CAL_ID = "c_6ed17073345c64d5b392f5a8ef7b4a62938f12c8fc5fecfa4b7256ef88acad28@group.calendar.google.com"
```

## Usage

Go to the ScheduleBuilder folder and run
```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```

Then go to the browser and enter the url **http://127.0.0.1:8000/**

# Sprint History (Development Process)

## Sprint 1 (Week 3 -> Week 6)
* Initial project planning
* Initial Django project setup
* Assignment parser
    - Upload assignment and parse out important information
* Syllabus parser
    - Upload syllabus and parse out important information 
* Initial Google Calendar API setup
    - Able to add events to calendar

## Sprint 2 (Week 7 -> Week 10)
* Improved UI
    - Nav bar
    - Login page
    - Home page
    - Canvas login page
* User login/registration
* Ability to delete events
* Additional options added to add event
    - Recurrence
    - Priority
* iCalendar API implementation

## Sprint 3 (Week 11 -> Week 15)
* Ability to edit events
* Friend system
    - Add friends
    - Remove friends
    - Add friends to events
* PyTest
    - Implementated unit tests for google calendar
