from django import forms

class LoginForm(forms.Form):
   user = forms.CharField(max_length = 100)
   password = forms.CharField(widget = forms.PasswordInput())

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)