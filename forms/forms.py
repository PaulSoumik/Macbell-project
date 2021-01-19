from django import forms
from forms.models import FreelancersProfile,CofounderProfile,EduDetails,CompanyBase,Products,JobOpening,SKILLS,JobApplication,WorkProfile,CofounderExperience
from forms.models import FundingPost,Franchisee,Franchisor,LookingForFranchise,InvestorProfile,InternProfile
from django.forms import formset_factory
from django.contrib.auth.models import User
class CofndProfileForm(forms.ModelForm):
     class Meta():
         model = CofounderProfile
         exclude = ('user',)

class skillform(object):
	class Meta():
		model = SKILLS

class EduDetailsform(forms.ModelForm):
	class Meta():
		model= EduDetails
		exclude = ('name',)








class FreelancersForm(forms.ModelForm):
     class Meta():
         model = FreelancersProfile
         fields = ['im','qualification','workingas','interestedin','lookingfor','skills','workpay','prevwork','industry','portfoliolink','about']












class CompanyBaseForm(forms.ModelForm):
	class Meta():
		model = CompanyBase
		fields = ('company_name','company_email','website','company_address','city','industry','businesstype','about_company')



		






class ProductForm(forms.ModelForm):
	class Meta():
		model = Products
		fields = ('prod_name','minimum_no','product_pic','price','description')







class JobOpeningForm(forms.ModelForm):
	class Meta():
		model = JobOpening
		fields = ('jobtilte','location','jobtype','experience','last_date','qualification','valid','reqskills')




class JobApplicationForm(forms.ModelForm):
	class Meta():
		model = JobApplication
		exclude = ('applicant','jobtilte',)


class WorkProfileForm(forms.ModelForm):
	class Meta():
		model = WorkProfile
		fields = ('Company_name','Post','Start_date','end_date')



WorkProfileFormset = formset_factory(WorkProfileForm, extra =1)





class CofounderExperienceForm(forms.ModelForm):
	class Meta():
		model = CofounderExperience
		fields = ('ex_company_name','job_post','starting_date','ending_date')
ExperienceFormset = formset_factory(CofounderExperienceForm, extra =1)




class InternForm(forms.ModelForm):
     class Meta():
         model = InternProfile
         exclude = ['user']

class InvestorForm(forms.ModelForm):
     class Meta():
         model = InvestorProfile
         exclude = ['user']
class FranchisorForm(forms.ModelForm):
     class Meta():
         model = Franchisor
         exclude = ['company_name']
class FranchiseeForm(forms.ModelForm):
     class Meta():
         model = Franchisee
         exclude = ['user','comapny_name']

class LookingForFranchiseForm(forms.ModelForm):
     class Meta():
         model = LookingForFranchise
         fields = '__all__'

class FundingPostForm(forms.ModelForm):
     class Meta():
         model = FundingPost
         exclude = ['company_name']
