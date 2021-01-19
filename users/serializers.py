from rest_framework import serializers
from users.models import UserProfile

from django.contrib.auth import get_user_model

User = get_user_model()



class userprofileserializer(serializers.ModelSerializer):
	
	class Meta:
		model = UserProfile
		fields = ['im','categories','profile_pic','lookingfor','address','contact','state','city','created_at','updated_at']

class userserializer(serializers.ModelSerializer):
	UserProfileInfo = userprofileserializer(many=False)
	class Meta:
		model = User
		fields = ['id','username','password','email','UserProfileInfo']


