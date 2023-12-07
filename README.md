# ScheduleBuilder
[![Build Django](https://github.com/ChicoState/ScheduleBuilder/blob/tidyup/.github/workflows/django.yml/badge.svg)](https://github.com/ChicoState/ScheduleBuilder/blob/tidyup/.github/workflows/django.yml)
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
