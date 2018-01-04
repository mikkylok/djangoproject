from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader
import MySQLdb
from MySQLdb import cursors

from django import forms
from models import User
from forms import RegisterForm,LoginForm
'''
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE":"djangoproject.settings")
django.setup()
'''

#Connect to MySQL
conn = MySQLdb.connect(host='localhost',user='root',passwd='',cursorclass=MySQLdb.cursors.DictCursor)
conn.select_db('djangoproject')
cursor = conn.cursor()

#Form
class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    email = forms.EmailField(label='Email')

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password',widget=forms.PasswordInput())


def register(request):
    if request.method == 'POST':
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            username = registerform.cleaned_data['username']
            password = registerform.cleaned_data['password']
            email = registerform.cleaned_data['email']
            new_user = User.objects.create(username=username,password=password,email=email)
            new_user.save()
            return HttpResponse("You have successfully registered an account.")
    else:
        registerform = RegisterForm()
    return render(request,'polls/register.html', {'registerform':registerform})

def login(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            password = loginform.cleaned_data['password']
            email = loginform.cleaned_data['email']
            user = User.objects.filter(email=email,password=password)
            if user:
                #HttpRepsonseRedirect Object
                response = HttpResponseRedirect('/polls/')
                response.set_cookie('email',email,3600)
                return response
            else:
                #alert?
                return HttpResponseRedirect('/login/')
    else:
        loginform = LoginForm()
    return render(request,'polls/login.html', {'loginform':loginform})

def logout(request):
    response = HttpRepsonse('Logout')
    response.delete_cookie('username')
    return response 

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
    if 'searchjob' in request.GET and 'searchpostcode' in request.GET:
        searchjob = request.GET['searchjob']
        searchpostcode = request.GET['searchpostcode']
        #message = 'You are searching for ' + searchjob
        cursor.execute("SELECT * FROM Repairman WHERE job LIKE '%%%s%%' and postcode LIKE '%%%s%%'"%(searchjob,searchpostcode))
        results = cursor.fetchall()
        if results != ():
            context = {'results':results}
            return render(request, 'polls/search_results.html', context)        
        else:
            return HttpResponse("No matched results.")
    else:
        message = 'Empty input!'
        return HttpResponse(message)
'''
def search(request):
    return HttpResponse("hello")
'''
