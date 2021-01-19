from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
import json
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from forms.models import CofounderProfile,EduDetails,CompanyBase,Products,SKILLS,JobApplication,JobOpening,WorkProfile,FreelancersProfile
from users.forms import UserForm,UserProfileForm
from users.models import FollowRelation,UserProfile
from forms.forms import FreelancersForm,CofndProfileForm,EduDetailsform,CompanyBaseForm,ProductForm,JobOpeningForm,WorkProfileForm,WorkProfileFormset,JobApplicationForm
from django.core import serializers
from django.contrib.auth.decorators import login_required
from forms.serializers import CompanyBasesrializer,JobOpeningSerializer,JobApplicationSerializer,FreelancersSerializer
from users.serializers import userserializer,userprofileserializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.urls import reverse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

import io

from django.db.models.query import EmptyQuerySet
from django.views import generic
# Create your views here.

from users.serializers import userserializer


@login_required
def user_logout(request):
    logout(request)
    return HttpResponse("logged out")




def register(request):
    registered = False
    flag =1
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        User = get_user_model()
        if user_form.is_valid() and profile_form.is_valid():
            for User in User.objects.filter():
            	if user_form.cleaned_data['email'] == User.email:
            		flag =0
            		user_form.cleaned_data['username'] = " "
            		print("This mail address already exists!")
     
            if flag ==1:
            	user = user_form.save()
            	print("user saved")
            	user.set_password(user.password)
            	user.save()
            	
            	profile = profile_form.save(commit=False)
            	profile.user = user

            	if 'profile_pic' in request.FILES:
            	    print('found it')
            	    profile.profile_pic = request.FILES['profile_pic']
            	profile.save()
            	registered = True
            else :
            	print("not-saved")
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'users/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered,
                           'flag':flag})






def Userlogin(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponse("logged in")
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'users/login.html', {})



from django.db.models import Q
def userlist(request):
	User = get_user_model()
	usersare = User.objects.exclude(username=request.user.username)
	following = FollowRelation.objects.filter(follower=request.user)
	for person in following:
		usersare = usersare.exclude(username=person.following.username)
	return render(request, 'users/userlist.html', {'usersare': usersare,'followingusers': following})


'''def follow(request,pk):
	User = get_user_model()
	following = User.objects.get(id = pk)
	follower = User.objects.get(username=request.user.username)
	print(following,follower)
	FollowRelation.objects.create(follower = follower, following= following)
	return HttpResponseRedirect(reverse('users:userlist'))'''

def following(request):
	User = get_user_model()
	following = FollowRelation.objects.filter(follower=request.user)
	return render(request, 'users/followingusers.html', {'followingusers': following})

'''def unfollow(request,pk):
	FollowRelation.objects.get(id=pk).delete()

	return HttpResponseRedirect(reverse('users:userlist'))'''




from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny


class UsersViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = userserializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)
    def list(self, request, *args, **kwargs):
        registered = False
        flag =1
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render(request,'users/registration.html',
                            {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered,
                           'flag':flag})
    def create(self, request, *args, **kwargs):
        registered = False
        flag =1
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        User = get_user_model()
        if user_form.is_valid() and profile_form.is_valid():
            for User in User.objects.filter():
                if user_form.cleaned_data['email'] == User.email:
                    flag =0
                    user_form.cleaned_data['username'] = " "
                    print("This mail address already exists!")
            if flag ==1:
                user = user_form.save()
                print("user saved")
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                if 'profile_pic' in request.FILES:
                    print('found it')
                    profile.profile_pic = request.FILES['profile_pic']
                profile.save()
                registered = True
            else :
                print("not-saved")
        else:
            print(user_form.errors,profile_form.errors)
        return render(request,'users/registration.html',
                            {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered,
                           'flag':flag})



class UserlistViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = userserializer
    authentication_classes = (TokenAuthentication,SessionAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def list(self, request, *args, **kwargs):
        User = get_user_model()
        following =[]
        usersare = User.objects.exclude(username=request.user.username)
        following = FollowRelation.objects.filter(follower=request.user)
        for person in following:
            usersare = usersare.exclude(username=person.following.username)
        for user in usersare:
            try:
                userfollow = following.get(following=user)
            except  FollowRelation.DoesNotExist:
                userfollow = None
        return render(request, 'users/userlist.html', {'usersare': usersare,'followingusers': following})



def follow(request,pk):
    User = get_user_model()
    following = User.objects.get(id = pk)
    follower = User.objects.get(username=request.user.username)
    print(following,follower)
    FollowRelation.objects.create(follower = follower, following= following)
    return HttpResponseRedirect(reverse('users:allusers-list'))


def unfollow(request,pk):
    FollowRelation.objects.get(id=pk).delete()

    return HttpResponseRedirect(reverse('users:allusers-list'))






class UserloginViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = userserializer
    authentication_classes = (TokenAuthentication,SessionAuthentication, )
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        return render(request, 'users/login.html', {})

    @action(detail=True,methods=['POST'])
    def Userlogin(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponse("logged in")
                else:
                    return HttpResponse("Your account was inactive.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return HttpResponse("Invalid login details given")