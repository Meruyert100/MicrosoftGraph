from tutorial.graphhelper import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta
from dateutil import tz, parser
from tutorial.authhelper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token, get_token

def home(request):
  context = initialize_context(request)

  return render(request, 'tutorial/home.html', context)

def initialize_context(request):
  context = {}

  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context

def sign_in(request):
  flow = get_sign_in_flow()
  try:
    request.session['auth_flow'] = flow
  except Exception as e:
    print(e)
  return HttpResponseRedirect(flow['auth_uri'])

def callback(request):
  result = get_token_from_code(request)

  user = get_user(result['access_token'])

  store_user(request, user)
  return HttpResponseRedirect(reverse('home'))

def sign_out(request):
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))

def images(request):
  context = initialize_context(request)

  images = {
      'images': get_images()
  }

  return render(request, 'tutorial/images.html', images)