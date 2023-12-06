"""
URL configuration for ScheduleBuilder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView, LoginView
from core import views as core_views
from google_calendar import views as cal_views
from account import views as acc_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('calendar/', cal_views.main, name='calendar'),
    path('icalendar/', cal_views.icalendar, name='icalendar-add'),
    path('calendar/add_assignment/',cal_views.add, name='calendar-add'),
    path('register/', acc_views.registration, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', core_views.user_login, name='login'),
    path('parser/', core_views.parser, name='parser'),
    path('accounts/', include('allauth.urls')),
    path('account/', include('account.urls', namespace='account')),
    path('search/', acc_views.account_search_view, name="search"),
    path('friend/', include('friend.urls', namespace='friend')),
    path('calendar/edit_assignment/', cal_views.edit_event, name='calender-edit'),
    path('calendar/edit/', cal_views.edit_event, name='edit_event'),
    path('update_event/', cal_views.edit_event, name='update_event'),
    path('calendar/delete_assignment/', cal_views.delete, name='calender-delete'),
    path('calendar/delete/',cal_views.delete, name='calendar-delete'),
]
