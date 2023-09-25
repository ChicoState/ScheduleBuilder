from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# for when we implement login features
from django.contrib.auth import authenticate, login, logout
from googleapiclient.errors import HttpError

def main(request):
    return render(request, 'core/home.html')
