from django import forms
from django.contrib.auth.models import User
#Form
class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30,error_messages={'required':u'Username can not be empty!'})
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(),error_messages={'required':u'Please input password!'})
    password2 = forms.CharField(label='Confirm your password', widget=forms.PasswordInput(),error_messages={'required':u'Please confirm your password!'})
    email = forms.EmailField(label='Email',error_messages={'required':u'Email can not be empty!'}) 
    phone = forms.CharField(label='Phone',max_length=20,error_messages={'required':u'Phone can not be empty!'})
    avatar = forms.ImageField(required=False,label='Profile picture', max_length=1024)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_username_exist = User.objects.filter(username=username).exists()
        if is_username_exist:
            raise forms.ValidationError("This username has been registered!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_email_exist = User.objects.filter(email=email).exists()
        if is_email_exist:
            raise forms.ValidationError("This email has been registered!")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password do not match!")
        return password2

'''
    def clean_avatar(self):
        filename = field.data.filename
        UPLOAD_FOLDER = ''
        ALLOWED_EXTENSIONS = ['png','jpg','jpeg','gif','PNG','JPG','JPEG','GIF']
        flag = '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
        if not flag:
            raise ValidationError('Invalid picture format!')
'''
 
class BeRepairmanForm(forms.Form):
    job = forms.CharField(label='Job', max_length=100,error_messages={'required':u'Job can not be empty!'})
    postcode = forms.CharField(label='Postcode', max_length=100,error_messages={'required':u'Postcode can not be empty!'})

     
'''
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
'''

