from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from google_calendar import views as cal_views
from profile import views as acc_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('calendar/', cal_views.calendar, name='calendar'),
    path('icalendar/', cal_views.icalendar, name='icalendar-add'),
    path('calendar/add_assignment/',cal_views.add, name='calendar-add'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', acc_views.registration, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('parser/', core_views.parser, name='parser'),
    path('account/', include('profile.urls', namespace='account')),
    path('search/', acc_views.account_search_view, name="search"),
    path('friend/', include('friend.urls', namespace='friend')),
    path('calendar/edit_assignment/', cal_views.edit_event, name='calender-edit'),
    path('calendar/edit/', cal_views.edit_event, name='edit_event'),
    path('update_event/', cal_views.edit_event, name='update_event'),
    path('calendar/delete_assignment/', cal_views.delete, name='calender-delete'),
    path('calendar/delete/',cal_views.delete, name='calendar-delete'),
]