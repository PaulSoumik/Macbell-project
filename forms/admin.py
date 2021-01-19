from django.contrib import admin
from django.contrib.admin import site, ModelAdmin

from forms.models import Franchisee,Franchisor,FundingPost,LookingForFranchise,InvestorProfile,InternProfile,FreelancersProfile,CofounderProfile,EduDetails,CompanyBase,Products,JobOpening,JobApplication,WorkProfile,SKILLS,CofounderExperience
#
# Register your models here.





admin.site.register(CofounderProfile)
admin.site.register(SKILLS)
admin.site.register(EduDetails)



admin.site.register(CompanyBase)


admin.site.register(Products)

admin.site.register(JobOpening)



admin.site.register(JobApplication)
admin.site.register(WorkProfile)




admin.site.register(FreelancersProfile)


admin.site.register(CofounderExperience)



admin.site.register(InternProfile)


admin.site.register(InvestorProfile)


admin.site.register(LookingForFranchise)

admin.site.register(Franchisor)

admin.site.register(Franchisee)

admin.site.register(FundingPost)