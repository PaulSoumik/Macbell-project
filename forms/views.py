from django.shortcuts import render, get_object_or_404
import json
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from forms.models import CofounderProfile,EduDetails,FundingPost,Franchisee,Franchisor,LookingForFranchise,InvestorProfile,InternProfile,CompanyBase,FundingPost,InternProfile,CofounderExperience,Products,SKILLS,JobApplication,JobOpening,WorkProfile,FreelancersProfile
from users.forms import UserForm,UserProfileForm
from forms.forms import FreelancersForm,CofndProfileForm,EduDetailsform,CompanyBaseForm,ProductForm,JobOpeningForm,WorkProfileForm,WorkProfileFormset,JobApplicationForm
from django.core import serializers
from django.contrib.auth.decorators import login_required
from forms.serializers import CompanyBasesrializer,JobOpeningSerializer,ProductSerializer,CofounderSerializer,JobApplicationSerializer,FreelancersSerializer,FundingSerializers,InternSerializer
from users.serializers import userserializer,userprofileserializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.urls import reverse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from forms.forms import CofounderExperienceForm,ExperienceFormset
import io

from django.db.models.query import EmptyQuerySet
from django.views import generic
from forms.serializers import FranchisorSerializer,LookingForFranchiseSerializer,FranchiseeSerializer,ProductSerializer,InvestorSerializer,InternSerializer,FundingSerializers
from forms.forms import InternForm,InvestorForm,FranchisorForm,FranchiseeForm,LookingForFranchiseForm,FreelancersForm,FundingPostForm

#Skills = []
Skills = SKILLS.objects.all()
#skills_js = serializers.serialize('json',Skills);
#skills_js = json.dumps(Skills)
skillsall = []










def index(request):
	for theskill in Skills.all():
		skillsall.append(theskill.name)
	CmpProducts = []
	cmp_reg = False;
	jobsavailable = []
	usercreatedjobs = []
	usercompany = None
	User = get_user_model()
	if request.user.is_authenticated:
		useris = User.objects.get(id=request.user.id);
		serializerdata = userserializer(instance = useris)
		jsondata = JSONRenderer().render(serializerdata.data)
		stream = io.BytesIO(jsondata)
		data = JSONParser().parse(stream)
		print("user data:")
		print(data)
		try:
			usercompany = CompanyBase.objects.get(user_id = request.user.id)
			cmpnyserialized = CompanyBasesrializer(instance= usercompany)
			print("user company serializer data:")
			cmpnydata =  JSONRenderer().render(cmpnyserialized.data)
			cmpnystream = io.BytesIO(cmpnydata)
			usercmpdata = JSONParser().parse(cmpnystream)
			print(usercmpdata)
		except CompanyBase.DoesNotExist:
			usercompany = None
		if usercompany:
			cmp_reg= False
			CmpProducts = Products.objects.filter(productcompany_id = usercompany.id)
		else:
			cmp_reg = True
		try:
			jobsavailable = []
			for job in JobOpening.objects.filter(valid= True):
				if job.job_companyname.user != request.user:
					jobsavailable.append(job)
					print(job)
				else:
					usercreatedjobs.append(job)
					print("user created job",job)
		except JobOpening.DoesNotExist:
			jobsavailable = None
	isjobsavailable = len(jobsavailable)
	return render(request,'forms/index.html',{'cmp_reg':cmp_reg,'CmpProducts':CmpProducts,'usercompany':usercompany,'isjobsavailable':isjobsavailable,'jobsavailable':jobsavailable,'usercreatedjobs':usercreatedjobs})


@login_required
def cofndprofile(request):
	useractive = False
	print("request found")
	companies = CompanyBase.objects.all()
	if request.method == 'POST':
		User = get_user_model()
		if request.user.is_authenticated:
			useractive = True
		cofn_form = CofndProfileForm(data= request.POST)
		experiences = ExperienceFormset(data = request.POST)
		print("data found")
		print(cofn_form,experiences)
		if cofn_form.is_valid() and experiences.is_valid() and useractive:
			userdata = User.objects.get(username = request.user.username)
			print(userdata.username , userdata.id, userdata.email)
			cofn =cofn_form.save(commit=False)
			cofn.user = userdata
			#print(cofn.skills)
			cofn.save()
			cofn_form.save_m2m()
			for exp in experiences:
				theexp = exp.save(commit=False)
				
				theexp.save()
				experience= get_object_or_404(CofounderExperience, id=theexp.id)
				cofounder= get_object_or_404(CofounderProfile, id=cofn.id)
				print(experience)
				cofounder.experience.add(experience)
				print('exp saved')
			cofounder.save()
			
			thecofounderprofile = CofounderProfile.objects.get(user = request.user)
			print("data saved")
		else:
			print(cofn_form.errors)
			print("not_vald")
		cofnform = CofndProfileForm()
		expform = ExperienceFormset()
		return render(request,'forms/cofndprofile.html',{'cofnform' : cofnform,'expform' : expform,'Skills' : Skills,"allskills": skillsall,"companies":companies})
	cofnform = CofndProfileForm()
	expform = ExperienceFormset()
	return render(request,'forms/cofndprofile.html',{'cofnform' : cofnform,'expform' : expform,'Skills' : Skills,"allskills": skillsall,"companies":companies})




def CompanyProfile(request):
	User = get_user_model()
	if request.method == 'POST':
			companybase_form = CompanyBaseForm(data=request.POST)
			print("Post method")
			if companybase_form.is_valid():
				print("forms valid")
				
				
				print("forms saved locally")
				if request.user.is_authenticated:
					print(request.user.username)
					theuser = User.objects.get(username = request.user.username)
					print(theuser.username , theuser.id, theuser.email)

					#companybase_form.user = theuser
					#companybase_form.user_id = theuser.id
					print("goint to loc save")
					companybase = companybase_form.save(commit=False)
					print("loc save")
					companybase.user = theuser
					print("companybase user done")
					print(companybase.user)
					
					print(companybase)
					companybase.save()

					print("company details are saved")
				else:
					print("user mot authenticated")
			else:
				print(companybase_form.errors)


	companybase_form = CompanyBaseForm()
	return render(request,'forms/company_profile.html',{'companybase_form':companybase_form} )




@csrf_exempt
def company_list(request):
	if request.method == 'GET':
		companies = FundingPost.objects.all()
		serializer = FundingSerializers(companies, many=True)
		return JsonResponse(serializer.data, safe=False)

	return JsonResponse(serializer.error,status=400)

@csrf_exempt
def intern_list(request):
	if request.method == 'GET':
		interns= InternProfile.objects.all()
		serializer = InternSerializer(interns, many=True)
		return JsonResponse(serializer.data, safe=False)

	return JsonResponse(serializer.error,status=400)


@csrf_exempt
def funding_list(request):
	if request.method == 'GET':
		fundings= FundingPost.objects.all()
		serializer = FundingSerializers(fundings, many=True)
		return JsonResponse(serializer.data, safe=False)

	return JsonResponse(serializer.error,status=400)







product_limit = 20;
@login_required
def addProduct(request):
	addpossible = True
	companyexist = True
	thatexist = 1
	company_is = None
	product_form = ProductForm()
	User = get_user_model()
	useris = User.objects.get(username = request.user.username)
	try:
		company_is = CompanyBase.objects.get(user_id = useris.id)
	except CompanyBase.DoesNotExist:
		company_is = None
		companyexist = False
		return render(request, 'forms/addproduct.html',{'product_form' : product_form,'thatexist':thatexist,'companyexist':companyexist,'addpossible':addpossible})
	if companyexist:
		products_num = Products.objects.filter(productcompany_id = company_is.id).count()
		if products_num >= product_limit:
			addpossible = False
			return render(request, 'forms/addproduct.html',{'product_form' : product_form,'thatexist':thatexist,'companyexist':companyexist,'addpossible':addpossible})
	
	if request.method == "POST":
		product = ProductForm(data = request.POST)
		print("product form saved")
		if product.is_valid():
			print("product form is valid")
			product_tosave = product.save(commit=False)
			print("product is new and locally saved")
			product_tosave.productcompany = company_is
			print("product company assigned")
			if 'product_pic' in request.FILES:
				product_tosave.product_pic = request.FILES['product_pic']
			print(product_tosave)
			print(product_tosave.productcompany)
			product_tosave.save()
			thatexist =2
			print("product saved")
		else:
			print(product.errors)
			if Products.objects.filter(productcompany_id = company_is.id).filter(Prod_name=product.data['Prod_name']):
				print("product already exists")
				thatexist = 0

	product_form = ProductForm()
	return render(request, 'forms/addproduct.html',{'product_form' : product_form,'thatexist':thatexist,'companyexist':companyexist,'addpossible':addpossible})




def editproddetails(request, pk):
	theproduct = None
	print(pk)
	theproduct = get_object_or_404(Products,pk=pk)
	print(pk)
	print(theproduct)
	response ={}
	response['productid'] = theproduct.id
	product_form = ProductForm(request.POST or None, instance= theproduct)
	print(product_form)
	if product_form.is_valid():
		prodname = request.POST['Prod_name']
		proddesc = request.POST['Description']
		print(prodname,proddesc)
		theproduct = product_form.save(commit=False)
		theproduct.save()
		return render(request, 'forms/editdone.html')
	else:
		print("not post")
		#return render(request, 'forms/editdone.html')Prod_name = theproduct.Prod_name,Description = theproduct.Description
	product_form = ProductForm()
	return render(request, 'forms/editproduct.html',{'product_form' : product_form,'theproduct':theproduct},response)






@login_required
def CreateJob(request):
	jobform = JobOpeningForm()
	companynotfound = False
	User = get_user_model()
	useris = User.objects.get(username = request.user.username)
	if request.method == "POST":
		jobformdata = JobOpeningForm(data= request.POST)
		print(jobformdata)
		print("job data is: ")
		company_is = None
		try:
			company_is = CompanyBase.objects.get(user_id = useris.id)
		except CompanyBase.DoesNotExist:
			company_is = None
		if jobformdata.is_valid():
			newjob = jobformdata.save(commit=False)
			if company_is == None:
				companynotfound = True
				return render(request, 'forms/createjob.html',{'jobform':jobform,'Skills' : Skills,'companynotfound':companynotfound})
			newjob.ForCompany = company_is
			newjob.save()
			jobformdata.save_m2m()

	return render(request, 'forms/createjob.html',{'jobform':jobform,'Skills' : Skills,'companynotfound':companynotfound})





@csrf_exempt
def Jobs_list(request):
	if request.method == 'GET':
		companies = JobOpening.objects.all()
		serializer = JobOpeningSerializer(companies, many=True)
		return JsonResponse(serializer.data, safe=False)

	return JsonResponse(serializer.error,status=400)



def applicants_list(request):
	if request.method == 'GET':
		applications = JobApplication.objects.all()
		serializer = JobApplicationSerializer(applications, many=True)
		return JsonResponse(serializer.data, safe=False)

	return JsonResponse(serializer.error,status=400)





def freelancersform(request):
	freelancersform = FreelancersForm();
	if request.method == 'POST':
		freelancersform = FreelancersForm(data= request.POST)
		if freelancersform.is_valid() :
			freelancer = freelancersform.save(commit=False)
			freelancer.theuser = request.user
			freelancer.save()
			freelancersform.save_m2m()

			return HttpResponseRedirect(reverse('index'))
		else:
			print(freelancersform.errors)
		
	return render(request, 'forms/freelancers.html',{'freelancersform':freelancersform,'Skills' : Skills})




from rest_framework.request import Request
@csrf_exempt
def freelancers_list(request):
	
	if request.method == 'GET':
		
		freelancers = FreelancersProfile.objects.all()
		serializer = FreelancersSerializer(freelancers, many=True)
		print(serializer.data)
		return JsonResponse(serializer.data, safe=False)

	return JsonResponse(serializer.error,status=400)


@csrf_exempt
def cofounder_list(request):
	
	if request.method == 'GET':
		
		cofounders = CofounderProfile.objects.all()
		serializer = CofounderSerializer(cofounders, many=True)
		print(serializer.data)
		return JsonResponse(serializer.data, safe=False)

	return JsonResponse(serializer.error,status=400)




@login_required
def applyforjob(request , pk):
	User = get_user_model()
	useris = User.objects.get(username = request.user.username)
	pass
	if request.method == "GET":
		jobapplyform = JobApplicationForm(request.GET or None)
		workset = WorkProfileFormset(request.GET or None)
	elif request.method == "POST":
		print("Post method detected")
		jobapplyformdata = JobApplicationForm(request.POST,request.FILES)
		worksetdata = WorkProfileFormset(data=request.POST)
		print("form data stored loclly")
		jobdetails = JobOpening.objects.get(pk = pk)
		print("job details selected",jobdetails)
		if jobapplyformdata.is_valid() and worksetdata.is_valid():
			print("forms are valid")
			jobapplication = jobapplyformdata.save(commit=False)
			jobapplication.applicant = useris
			jobapplication.jobtilte = jobdetails
			print("jobtitle added")
			if 'resume' in request.FILES:
				print("resume found")
				jobapplication.resume = request.FILES['resume']
				print("resume added")
			jobapplication.save()
			print("jobapplication saved")
			jobapplications = JobApplication.objects.filter(jobtilte= jobapplication.jobtilte)
			thejobapplication = jobapplications.get(applicant = jobapplication.applicant)
			print(thejobapplication.id, thejobapplication)
			print(type(thejobapplication.id))
			for work in worksetdata:
				print(work)
				workprofile = work.save(commit=False)
				workprofile.jobapplication = thejobapplication
				workprofile.save()
				print("work saved:", workprofile.Company_name )
			print("jobapplication saved:", jobapplication.applicant)
		else:
			print(jobapplyformdata.errors,worksetdata.errors)

	jobapplyform = JobApplicationForm()
	workset = WorkProfileFormset()

	return render(request, 'forms/jobapplication.html', {'jobapplyform':jobapplyform, 'workset': workset})



@login_required
def applicants(request, pk):
	jobdetails = JobOpening.objects.get(pk = pk)
	alljobapplications = JobApplication.objects.filter(jobtilte = jobdetails)



	return render(request, 'forms/listapplicants.html',{'jobdetails':jobdetails,'alljobapplications':alljobapplications})



@login_required
def fullapplication(request , pk):
	fulljobapplication = JobApplication.objects.get(pk = pk)
	workexp = WorkProfile.objects.filter(jobapplication= fulljobapplication)

	return render(request, 'forms/fullapplication.html',{'fulljobapplication':fulljobapplication,'workexp':workexp})




#.....................................Viewsets....................................


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

class FreelancersViewSet(viewsets.ModelViewSet):
    queryset = FreelancersProfile.objects.all()
    serializer_class = FreelancersSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def list(self, request, *args, **kwargs):
        freelancersform = FreelancersForm();
        return render(request, 'forms/freelancers.html',{'freelancersform':freelancersform,'Skills' : Skills},status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        freelancersform = FreelancersForm(data= request.POST)
        if freelancersform.is_valid() :
        	freelancer = freelancersform.save(commit=False)
        	freelancer.theuser = request.user
        	freelancer.save()
        	freelancersform.save_m2m()
        	return HttpResponseRedirect(reverse('index'))
        else:
        	print(freelancersform.errors)
        	return render(request, 'forms/freelancers.html',{'freelancersform':freelancersform,'Skills' : Skills},status=status.HTTP_400_BAD_REQUEST)




#company profile
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = CompanyBase.objects.all()
    serializer_class = CompanyBasesrializer
    authentication_classes = (TokenAuthentication,SessionAuthentication,  )
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def list(self, request, *args, **kwargs):
    	User = get_user_model()
    	companybase_form = CompanyBaseForm()
    	return render(request,'forms/company_profile.html',{'companybase_form':companybase_form} )

    def create(self, request, *args, **kwargs):
        companybase_form = CompanyBaseForm(data=request.POST)
        if companybase_form.is_valid():
            if request.user.is_authenticated:
                theuser = User.objects.get(username = request.user.username)
                companybase = companybase_form.save(commit=False)
                companybase.user = theuser
                companybase.save()

                print("company details are saved")
            else:
                print("user mot authenticated")
        else:
            print(companybase_form.errors)



#cofounder profile
class CofounderViewSet(viewsets.ModelViewSet):
    queryset = CofounderProfile.objects.all()
    serializer_class = CofounderSerializer
    authentication_classes = (TokenAuthentication,SessionAuthentication,  )
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def list(self, request, *args, **kwargs):
        cofnform = CofndProfileForm()
        companies = CompanyBase.objects.all()
        expform = ExperienceFormset()
        eduform = EduDetailsform()
        return render(request,'forms/cofndprofile.html',{'cofnform' : cofnform,'expform' : expform,'eduform': eduform,'Skills' : Skills,"allskills": skillsall,"companies":companies})


    def create(self, request, *args, **kwargs):
        useractive = False
        companies = CompanyBase.objects.all()
        if request.method == 'POST':
        	User = get_user_model()
        	if request.user.is_authenticated:
        		useractive = True
        	cofn_form = CofndProfileForm(data= request.POST)
        	edu = EduDetailsform(data= request.POST)
        	experiences = ExperienceFormset(data = request.POST)
        	if cofn_form.is_valid() and experiences.is_valid() and useractive and edu.is_valid():
        		education = edu.save(commit=False)
        		userdata = User.objects.get(username = request.user.username)
        		education.name = userdata
        		education.save()
        		print("education saved")
        		print(education.id)
        		cofn =cofn_form.save(commit=False)
        		cofn.user = userdata
        		educationis = EduDetails.objects.get(id=education.id)
        		cofn.education = educationis
        		cofn.save()
        		cofn_form.save_m2m()
        		for exp in experiences:
        			theexp = exp.save(commit=False)
        			theexp.save()
        			experience= get_object_or_404(CofounderExperience, id=theexp.id)
        			cofounder= get_object_or_404(CofounderProfile, id=cofn.id)
        			cofounder.experience.add(experience)
        		cofounder.save()
        		thecofounderprofile = CofounderProfile.objects.get(user = request.user)
        		return HttpResponseRedirect(reverse('index'))
        	else:
        		print(cofn_form.errors)
        		cofnform = CofndProfileForm()
        		companies = CompanyBase.objects.all()
        		expform = ExperienceFormset()
        		eduform = EduDetailsform()
        		return render(request,'forms/cofndprofile.html',{'cofnform' : cofnform,'expform' : expform,'eduform': eduform,'Skills' : Skills,"allskills": skillsall,"companies":companies})



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,SessionAuthentication,  )
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):

    	addpossible = True
    	companyexist = True
    	thatexist = 1
    	company_is = None
    	product_form = ProductForm()
    	User = get_user_model()
    	useris = User.objects.get(username = request.user.username)
    	try:
    		company_is = CompanyBase.objects.get(user_id = useris.id)
    	except CompanyBase.DoesNotExist:
    		company_is = None
    		companyexist = False
    		return render(request, 'forms/addproduct.html',{'product_form' : product_form,'thatexist':thatexist,'companyexist':companyexist,'addpossible':addpossible})
    	if companyexist:
    		products_num = Products.objects.filter(productcompany_id = company_is.id).count()
    		if products_num >= product_limit:
    			addpossible = False
    			return render(request, 'forms/addproduct.html',{'product_form' : product_form,'thatexist':thatexist,'companyexist':companyexist,'addpossible':addpossible})
    	product_form = ProductForm()
    	return render(request, 'forms/addproduct.html',{'product_form' : product_form,'thatexist':thatexist,'companyexist':companyexist,'addpossible':addpossible})
    def create(self, request, *args, **kwargs):
    	addpossible = True
    	companyexist = True
    	thatexist = 1
    	company_is = None
    	User = get_user_model()
    	useris = User.objects.get(username = request.user.username)
    	company_is = CompanyBase.objects.get(user_id = useris.id)
    	if request.method == "POST":
    		product = ProductForm(data = request.POST)
    		print("product form saved")
    		if product.is_valid():
    			print("product form is valid")
    			product_tosave = product.save(commit=False)
    			print("product is new and locally saved")
    			product_tosave.productcompany = company_is
    			print("product company assigned")
    			if 'product_pic' in request.FILES:
    				product_tosave.product_pic = request.FILES['product_pic']
    			print(product_tosave)
    			print(product_tosave.productcompany)
    			product_tosave.save()
    			thatexist =2
    			print("product saved")
    		else:
    			print(product.errors)
    			if Products.objects.filter(productcompany_id = company_is.id).filter(Prod_name=product.data['Prod_name']):
    				print("product already exists")
    				thatexist = 0
    	product_form = ProductForm()
    	return render(request, 'forms/addproduct.html',{'product_form' : product_form,'thatexist':thatexist,'companyexist':companyexist,'addpossible':addpossible})


	
class EditProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,SessionAuthentication,  )
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def list(self, request,prod_pk, *args, **kwargs):
    	product_form = ProductForm()
    	theproduct = None
    	print(prod_pk)
    	theproduct = get_object_or_404(Products,pk=prod_pk)
    	print(prod_pk)
    	print(theproduct)
    	response ={}
    	response['productid'] = theproduct.id
    	return render(request, 'forms/editproduct.html',{'product_form' : product_form,'theproduct':theproduct},response)


    def create(self, request,prod_pk, *args, **kwargs):
    	theproduct = None
    	print(prod_pk)
    	theproduct = get_object_or_404(Products,pk=prod_pk)
    	print(prod_pk)
    	print(theproduct)
    	response ={}
    	
    	response['productid'] = theproduct.id
    	if request.POST['prod_name']:
    		theproduct.prod_name = request.POST['prod_name']
    	if request.POST['minimum_no']:
    		theproduct.minimum_no = request.POST['minimum_no']
    	if request.POST['price']:
    		theproduct.price = request.POST['price']
    	if request.POST['description']:
    		theproduct.description = request.POST['description']
    	if 'product_pic' in request.FILES:
    		theproduct.product_pic = request.FILES['product_pic']
    	
    	#prod_name = request.POST['prod_name']
    	#description = request.POST['description']
    	#minimum_no = request.POST['minimum_no']
    	
    	theproduct.save()
    	return render(request, 'forms/editdone.html')
    	product_form = ProductForm()
    	return render(request, 'forms/editproduct.html',{'product_form' : product_form,'theproduct':theproduct},response)


class JobOpeningViewSet(viewsets.ModelViewSet):
	queryset = JobOpening.objects.all()
	serializer_class = JobOpeningSerializer
	authentication_classes = (TokenAuthentication,SessionAuthentication,  )
	permission_classes = (IsAuthenticatedOrReadOnly,)
	def list(self, request, *args, **kwargs):
		jobform = JobOpeningForm()
		companynotfound = False
		User = get_user_model()
		useris = User.objects.get(username = request.user.username)
		company_is = None
		try:
			company_is = CompanyBase.objects.get(user_id = useris.id)
		except CompanyBase.DoesNotExist:
			company_is = None
		if company_is == None:
			companynotfound =True
		return render(request, 'forms/createjob.html',{'jobform':jobform,'Skills' : Skills,'companynotfound':companynotfound})

	def create(self, request, *args, **kwargs):
		jobformdata = JobOpeningForm(data= request.POST)
		User = get_user_model()
		useris = User.objects.get(username = request.user.username)
		companynotfound = False
		company_is = None
		try:
			company_is = CompanyBase.objects.get(user_id = useris.id)
		except CompanyBase.DoesNotExist:
			company_is = None
		if jobformdata.is_valid():
			newjob = jobformdata.save(commit=False)
			newjob.job_companyname = company_is
			newjob.save()
			jobformdata.save_m2m()
			return HttpResponse("job opened") 
		else:
			print(jobformdata.errors)
			return HttpResponse("job not opened")



class FranchisorViewSet(viewsets.ModelViewSet):
	queryset = Franchisor.objects.all()
	serializer_class = FranchisorSerializer
	authentication_classes = (TokenAuthentication,SessionAuthentication,  )
	permission_classes = (IsAuthenticatedOrReadOnly,)
	def list(self, request, *args, **kwargs):
		franchisorform = FranchisorForm()
		User = get_user_model()
		useris = User.objects.get(username = request.user.username)
		companyexist = True
		company_is = None
		products =None
		try:
			company_is = CompanyBase.objects.get(user_id = useris.id)
		except CompanyBase.DoesNotExist:
			company_is = None
			companyexist = False
		if company_is:
			products = Products.objects.filter(productcompany=company_is)
		return render(request,'forms/Franchisor.html',{'franchisorform' : franchisorform,'Skills' : Skills,'companyexist' : companyexist,'products':products})


	def create(self, request, *args, **kwargs):
		franchisorform = FranchisorForm(data=request.POST)
		User = get_user_model()
		useris = User.objects.get(username = request.user.username)
		companyexist = True
		company_is = None
		products =None
		company_is = CompanyBase.objects.get(user_id = useris.id)
		if franchisorform.is_valid():
			franchisor = franchisorform.save(commit=False);
			franchisor.company_name = company_is
			franchisor.save()
			return HttpResponse("saved")
		else:
			print(franchisorform.errors)
			return HttpResponse("not saved. Data is not valid")








class FranchiseeViewSet(viewsets.ModelViewSet):
	queryset = Franchisee.objects.all()
	serializer_class = FranchiseeSerializer
	authentication_classes = (TokenAuthentication,SessionAuthentication,  )
	permission_classes = (IsAuthenticatedOrReadOnly,)
	def list(self, request, *args, **kwargs):
		franchiseeform = FranchiseeForm()
		User = get_user_model()
		useris = User.objects.get(username = request.user.username)
		companyexist = True
		company_is = None
		products =None
		print(franchiseeform)
		try:
			company_is = CompanyBase.objects.get(user_id = useris.id)
		except CompanyBase.DoesNotExist:
			company_is = None
			companyexist = False
		lookigforfranchisee = LookingForFranchise.objects.all();
		return render(request,'forms/Franchisee.html',{'franchiseeform' : franchiseeform,'Skills' : Skills,'companyexist' : companyexist,'lookigforfranchisee':lookigforfranchisee})


	def create(self, request, *args, **kwargs):
		franchiseeform = FranchiseeForm(data=request.POST)
		User = get_user_model()
		useris = User.objects.get(username = request.user.username)
		companyexist = True
		company_is = None
		products =None
		try:
			company_is = CompanyBase.objects.get(user_id = useris.id)
		except CompanyBase.DoesNotExist:
			company_is = None
		print(company_is)
		if franchiseeform.is_valid():
			franchisee = franchiseeform.save(commit=False);
			franchisee.user = useris
			franchisee.comapny_name = company_is
			print(franchisee.comapny_name)
			if 'logo' in request.FILES:
				franchisee.logo = request.FILES['logo'];
			franchisee.save()
			return HttpResponse("saved")
		else:
			print(franchiseeform.errors)
			return HttpResponse("not saved. Data is not valid")


class InternViewSet(viewsets.ModelViewSet):
	queryset = InternProfile.objects.all()
	serializer_class = InternSerializer
	authentication_classes = (TokenAuthentication,SessionAuthentication,  )
	permission_classes = (IsAuthenticatedOrReadOnly,)
	def list(self, request, *args, **kwargs):
		internform = InternForm()
		return render(request,'forms/intern.html',{'internform' : internform,'Skills' : Skills})


	def create(self, request, *args, **kwargs):
		internform = InternForm(data=request.POST)
		User = get_user_model()
		useris = User.objects.get(username = request.user.username)
		print(useris)
		if internform.is_valid():
			internis = internform.save(commit=False);
			internis.user = useris
			internis.save()
			internform.save_m2m()
			return HttpResponse("saved")
		else:
			print(internform.errors)
			return HttpResponse("not saved. Data is not valid")



class FundingViewSet(viewsets.ModelViewSet):
	queryset = FundingPost.objects.all()
	serializer_class = FundingSerializers
	authentication_classes = (TokenAuthentication,SessionAuthentication,  )
	permission_classes = (IsAuthenticatedOrReadOnly,)
	def list(self, request, *args, **kwargs):
		fundingpostform = FundingPostForm()
		User = get_user_model()
		useris = User.objects.get(username = request.user.username)
		companyexist = True
		company_is = None
		
		try:
			company_is = CompanyBase.objects.get(user_id = useris.id)
		except CompanyBase.DoesNotExist:
			company_is = None
			companyexist = False
		
		return render(request,'forms/funding.html',{'fundingpostform' : fundingpostform,'Skills' : Skills,'companyexist' : companyexist})


	def create(self, request, *args, **kwargs):
		fundingpostform = FundingPostForm(data=request.POST)
		User = get_user_model()
		useris = User.objects.get(username = request.user.username)
		companyexist = True
		company_is = None
		products =None
		company_is = CompanyBase.objects.get(user_id = useris.id)
		if fundingpostform.is_valid():
			funding = fundingpostform.save(commit=False);
			funding.company_name = company_is
			funding.save()
			return HttpResponse("saved")
		else:
			print(fundingpostform.errors)
			return HttpResponse("not saved. Data is not valid")

