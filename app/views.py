import os
from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import json
import re
from django.http import JsonResponse


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
            return redirect('logout')
        else:
            return render(request, 'index.html')
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        pattern = r"^\S+@\S+\.\S+$"
        if re.match(pattern, email):
            print('matched')
            try:
                user_object = UserDetails.objects.get(email=email)
            except UserDetails.DoesNotExist:
                user_object = None
            if user_object:
                print('user exist')
                unew = UserDetails.objects.get(email=email)
                checked = unew.pass_word
                if checked == password:
                    print('password success')
                    RTO = 'RTO'
                    if UserDetails.objects.filter(email=unew.email, pass_word=checked, account_type=RTO).exists():
                        user_id = UserDetails.objects.get(
                            email=request.POST['email'], pass_word=request.POST['password'])
                        request.session['user_id'] = user_id.id
                        print('RTO')
                        return redirect('RTO')

                    user = 'user'
                    if UserDetails.objects.filter(email=email, pass_word=password, account_type=user).exists():
                        user_id = UserDetails.objects.get(
                            email=request.POST['email'], pass_word=request.POST['password'])
                        request.session['user_id'] = user_id.id
                        print('user')
                        return redirect('user')

                    agent = 'agent'
                    if UserDetails.objects.filter(email=email, pass_word=password, account_type=agent).exists():
                        user_id = UserDetails.objects.get(
                            email=request.POST['email'], pass_word=request.POST['password'])
                        request.session['user_id'] = user_id.id
                        print('agent')
                        return redirect('agent')
                    else:
                        return redirect('index')
                else:
                    email = request.POST['email']
                    passerr = "password Incorrect!"
                    print("password Incorrect!")
                    return render(request, 'index.html', {'passerr': passerr, 'email': email})
            else:
                noemailerr = request.POST['email']
                return render(request, 'index.html', {'noemailerr': noemailerr})
        else:
            email = request.POST['email']
            emailerr = 'invalid email'
            print('invalid email')
            return render(request, 'index.html', {'emailerr': emailerr, 'email': email})
    else:
        print('what?!')
        return redirect('index')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def RTO(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
        else:
            return redirect('index')
        RTO = UserDetails.objects.filter(id=user_id)
        return render(request, 'RTO.html', {'RTO': RTO})
    else:
        return redirect('/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
            user = UserDetails.objects.filter(id=user_id)
            return render(request, 'user.html', {'user': user})
        else:
            return redirect('index')
    else:
        return redirect('index')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def agent(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
            agent = UserDetails.objects.filter(id=user_id)
            return render(request, 'agent.html', {'agent': agent})
        else:
            return redirect('index')
    else:
        return redirect('index')


def logout(request):
    if 'user_id' in request.session:
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')
