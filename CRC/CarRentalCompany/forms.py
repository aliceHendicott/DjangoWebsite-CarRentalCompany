from django import forms
from django.contrib.auth import (authenticate, login, get_user_model, logout)
import datetime

User = get_user_model()
#
# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput)
#     def clean(self, *args, **kwargs):
#         username = self.cleaned_data['username']
#         password = self.cleaned_data['password']
#         if username and password:
#             user = authenticate(username=username, password=password)
#             if not user:
#                 raise forms.ValidationError("This user does not exist")
#             if not user.check_password(password):
#                 raise forms.ValidationError("Incorrect Password")
#             if not user.is_active:
#                 raise forms.ValidationError("This user is no longer active")
#             return super(LoginForm, self).clean(*args, **kwargs)

class RecommendForm(forms.Form):
    purposeOptions = (("1", "Four wheel Driving"), ("2", "Family trip"), ("3", "Road Trip"))
    purpose = forms.ChoiceField(choices=purposeOptions)
    seatsOptions = (("1", "1 or 2"), ("2", "3 - 5"), ("3", "more than 5"))
    seats = forms.ChoiceField(choices=seatsOptions)
    transmissionOptions = (("1", "Automatic"), ("2", "Manual"))
    transmission = forms.ChoiceField(choices=transmissionOptions)
    monthOptions = (("1", "January"), ("2", "February"), ("3", "March"), ("4", "April"), ("5", "May"),
                    ("6", "June"), ("7", "July"), ("8", "August"), ("9", "September"), ("10", "October"),
                    ("11", "November"), ("12", "December"))
    month = forms.ChoiceField(choices=monthOptions)
    def clean(self):
        purpose = forms.cleaned_data['purpose']
        seats = forms.cleaned_data['seats']
        transmission = forms.cleaned_data['transmission']
        month = forms.cleaned_data['month']
        if purpose or seats or transmission or month:
            return super(RecommendForm, self).clean()
