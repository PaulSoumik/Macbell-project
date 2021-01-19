from django.contrib import admin

# Register your models here.
from users.models import UserProfile,FollowRelation,LookingFor



admin.site.register(UserProfile)
admin.site.register(FollowRelation)
admin.site.register(LookingFor)