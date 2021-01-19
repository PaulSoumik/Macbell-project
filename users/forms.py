from django.contrib.auth.models import User
from django import forms
from users.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')
class UserProfileForm(forms.ModelForm):
     class Meta():
         model = UserProfile
         fields = ('im','categories','profile_pic','lookingfor','address','contact','country','state','city')



