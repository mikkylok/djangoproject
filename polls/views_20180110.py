# -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader
import MySQLdb
from MySQLdb import cursors

from forms import RegisterForm, BeRepairmanForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from models import UserProfile

from django.contrib import messages
from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
'''
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE":"djangoproject.settings")
django.setup()
'''

#Connect to MySQL
conn = MySQLdb.connect(host='localhost',user='root',passwd='',cursorclass=MySQLdb.cursors.DictCursor)
conn.select_db('djangoproject')
cursor = conn.cursor()

def register(request):
    #current_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()); 
    if request.method == 'POST':
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            registerinfo = registerform.cleaned_data
            username = registerinfo['username']
            password = registerinfo['password1']
            email = registerinfo['email']
            phone = registerinfo['phone']
            #avatar = registerinfo['avatar']
            #destination = open(avatar.name, 'wb+')
            #for chunk in avatar.chunks():
            #    destination.write(chunk)
            #destination.close()
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            if request.FILES:
                avatar = request.FILES['avatar']
                avatar.name = str(new_user.id) + '.' + avatar.name.split('.')[1]
                profile = UserProfile(phone=phone,avatar=avatar,user=new_user)
            else:
                profile = UserProfile(phone=phone,user=new_user) 
               #why cant profile = UserProfile.objects.create(phone=phone,user=new_user)
            profile.save()
            return HttpResponseRedirect('/polls/')        
    else:
        registerform = RegisterForm()
    return render(request,'polls/register.html', {'registerform':registerform})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None and user.is_active:
            login(request, user)
            request.session['username'] = username
            return HttpResponseRedirect('/polls/')                #response.
        else:
            context = {"loggedin": False}
            return render(request, "polls/login.html", context)
    else:
        context = {"loggedin": True}
    return render(request, "polls/login.html", context)

 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/polls/')

# Create your views here.
def index(request):
   # cursor.execute("SELECT name FROM Repairman WHERE id=3")
   # name = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM Repairman")
    results = cursor.fetchall()
    #response = ""
    #for result in results:
    #     response += "id is %d,name is %s, job is %s, postcode is %d\n" %result
   # template = loader.get_template('polls/index.html')
    context = {'results':results}
   # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def search(request):
    if 'job' in request.GET and 'postcode' in request.GET:
        searchjob = request.GET['job']
        searchpostcode = request.GET['postcode']
        #message = 'You are searching for ' + searchjob
        cursor.execute("SELECT repairman.job,repairman.postcode,auth_user.username,auth_user.email FROM repairman,auth_user WHERE repairman.user_id=auth_user.id and job LIKE '%%%s%%' and postcode LIKE '%%%s%%'"%(searchjob,searchpostcode))
        results = cursor.fetchall()
        if results != ():
            paginator = Paginator(results,2)
            page = request.GET.get('page')
            try:
                current_page = paginator.page(page)
                repairmen = current_page.object_list
            except PageNotAnInteger:
                current_page = paginator.page(1)
                repairmen = current_page.object_list
            except EmptyPage:
                current_page = paginator.page(paginator.num_pages)
                repairmen = current_page.object_list
            return render(request,"polls/search_results.html",{"repairmen":repairmen,"page":current_page, "job":searchjob,"postcode":searchpostcode})
        else:
            return HttpResponse("No Matched results.")
    else:
        message = "Empty input!"
        return HttpResponse(message)
'''
        if results != ():
            context = {'results':results}
            return render(request, 'polls/search_results.html', context)        
        else:
            return HttpResponse("No matched results.")
    else:
        message = 'Empty input!'
        return HttpResponse(message)
'''
'''
def search(request):
    return HttpResponse("hello")
'''
def profile(request, user_id):
    userid = int(user_id.encode("utf-8"))
    user = User.objects.get(id=user_id)
    context = {'user':user}
    return render(request,'polls/profile.html',context)
'''
    cursor.execute("SELECT * FROM auth_user WHERE id='%d'"%userid)
    profile = cursor.fetchone()
    context = {'profile':profile}
    return render(request, 'polls/profile.html', context)
'''
def berepairman(request): 
    if request.method == 'POST':
        berepairmanform = BeRepairmanForm(request.POST)
        if berepairmanform.is_valid():
            repairmaninfo = berepairmanform.cleaned_data
            job = repairmaninfo['job']
            postcode = repairmaninfo['postcode']
            cursor.execute("INSERT INTO repairman(job,postcode,user_id)VALUES('%s','%s','%s')"%(job,postcode,request.user.id))
            conn.commit()
            messages.success(request,'You have successfully registered to be a repairman!')
            return HttpResponseRedirect('/polls/')
    else:
        berepairmanform = BeRepairmanForm()
    return render(request,'polls/berepairman.html', {'berepairmanform':berepairmanform})
