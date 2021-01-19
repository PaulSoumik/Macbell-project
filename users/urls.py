from django.contrib import admin
from django.urls import path

from rest_framework.routers import SimpleRouter
from django.conf.urls import url,include
from users import views
from users.views import UsersViewSet,UserloginViewSet,UserlistViewSet
# SET THE NAMESPACE!
app_name = 'users'
userrouter = SimpleRouter()
userrouter.register("Usersignup",UsersViewSet,'signupuser')
userrouter.register("userlogin",UserloginViewSet,'userlogin')
userrouter.register("allusers",UserlistViewSet,'allusers')

urlpatterns=[
	url(r'^signup/$',views.register,name='register'),
    url(r'^login/$',views.Userlogin,name='login'),
    url(r'^logout/$',views.user_logout,name='logout'),
    url(r'^userlist/$',views.userlist,name='userlist'),
    url(r'^followed/(?P<pk>.*)/$',views.follow,name='follow'),
    url(r'^following/$',views.following,name='following'),
    url(r'^unfollowed/(?P<pk>.*)/$',views.unfollow,name='unfollow'),
    url(r'^',include(userrouter.urls))
    ]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)