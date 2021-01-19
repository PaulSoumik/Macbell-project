from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from django.conf.urls import url,include
from forms import views
from forms.views import FreelancersViewSet,CompanyViewSet,CofounderViewSet,ProductViewSet,EditProductViewSet,JobOpeningViewSet,FundingViewSet,InternViewSet,FranchiseeViewSet,FranchisorViewSet
# SET THE NAMESPACE!
app_name = 'forms'
router = SimpleRouter()
router.register("freelancersprofile",FreelancersViewSet)
router.register("createcompany",CompanyViewSet,'createcompany')
router.register("createcofounder",CofounderViewSet,'createcofounder')
router.register("addnewproduct",ProductViewSet,'addnewproduct')
router.register("jobopening",JobOpeningViewSet,'jobopening')
router.register("intern",InternViewSet,'intern')
router.register("franchisee",FranchiseeViewSet,'franchisee')
router.register("franchisor",FranchisorViewSet,'franchisor')
router.register("fundingpost",FundingViewSet,'fundingpost')
router.register("edittheproduct/(?P<prod_pk>.*)",EditProductViewSet,'edittheproduct')

urlpatterns=[
    url(r'^cofndprofile/$',views.cofndprofile,name='cofndprofile'),
    url(r'^Company_profile/$',views.CompanyProfile,name='Company_profile'),
    url(r'^Add_Products/$',views.addProduct,name='addproduct'),
    url(r'^CreateJob/$',views.CreateJob,name='createjob'),
    url(r'^productedit/(?P<pk>.*)/$',views.editproddetails,name='editproductdetails'),
    url(r'^JobApplication/(?P<pk>.*)/$',views.applyforjob,name='joobapplication'),
    url(r'^ApplicantsList/(?P<pk>.*)/$',views.applicants,name='applicantslist'),
    url(r'^FullApplication/(?P<pk>.*)/$',views.fullapplication,name='fullapplication'),
    url(r'^freelancersform/',views.freelancersform,name='freelancersform'),
    url(r'^companies/',views.company_list,name='company_list'),
    url(r'^jobs/',views.Jobs_list,name='Jobs_list'),
    url(r'^jobapplicants/',views.applicants_list,name='applicants_list'),
    url(r'^freelancers/',views.freelancers_list,name='freelancers'),
    url(r'^cofounders/',views.cofounder_list,name='cofounders'),
    url(r'^interns/',views.intern_list,name='interns'),
    url(r'^fundings/',views.funding_list,name='fundings'),
    url(r'^',include(router.urls))

    ]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)