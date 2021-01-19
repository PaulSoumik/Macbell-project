from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

#indiv = [('student','student'), ('enterpreneur','enterpreneur'), ('Businessman','Businessman'),('Employee','Employee')]
#searching = [('startup-idea','startup-idea'), ('startup-company','startup-company')]
#joinas = [('cofounder','cofounder'),('team-member','team-member'),('partner','partner'),('others','others')]

profas = [('student','student'), ('enterpreneur','enterpreneur'), ('Businessman','Businessman'),('Investor','Investor'),('Freelancers','Freelancers'),('Student Enterpreneur','Student Enterpreneur')]

'''categories = [('Business Advisor','Business Advisor'),
				('Financial Advisor','Financial Advisor'),
				('Technical Advisor','Technical Advisor'),
				('Legal Advisor','Legal Advisor'),
				('Chater Accountant','Chater Accountant'),
				('Company secretary','Company secretary'),
				('Content Writter','Content Writter'),
				('Graphic Designer','Graphic Designer'),
				('Adv. Film Maker','Adv. Film Maker'),
				('Web Developer','Web Developer'),
				('Software Developer','Software Developer'),
				('App Developer','App Developer'),
				('Digital Marketing','Digital Marketing'),
				('Event Planner','Event Planner'),
				('Data Entry Operator','Data Entry Operator'),
				('Telecaller','Telecaller'),
				('Markeitng','Markeitng'),
				('Hr','Hr')]'''
categories = [('Freelancer','Freelancer'),('Investor','Investor'),('Intern/Employee','Intern/Employee'),('Co-founder','Co-founder'),('Franchisee','Franchisee')]

class LookingFor(models.Model):
	lookingfor = models.CharField(max_length=100,blank=True)
	def __str__(self):
		return self.lookingfor

class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='UserProfileInfo')
	im = models.CharField(max_length=100,blank=False,choices=profas)
	categories =  models.CharField(max_length=100,blank=False,choices=categories)
	profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
	lookingfor = models.ManyToManyField(LookingFor,blank=False)
	address = models.TextField(max_length=400,blank=True)
	contact = models.BigIntegerField(unique=True,blank=False)
	country = models.CharField(max_length=100,blank=True)
	state = models.CharField(max_length=100,blank=True) #change dropdown
	city = models.CharField(max_length=100,blank=True) #change dropdown
	created_at = models.DateTimeField(auto_now_add= True)
	updated_at = models.DateTimeField(auto_now= True)
	def __str__(self):
		return self.user.username



class FollowRelation(models.Model):
	follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower')
	following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
	def __str__(self):
		return self.follower.username
	def clean(self):
		print(self.following.username)
		if self.follower.username == self.following.username:
			raise ValidationError(('A person can not follow himself'))




from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)