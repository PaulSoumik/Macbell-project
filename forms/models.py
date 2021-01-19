from django.db import models
from django.contrib.auth.models import User

# Create your models here.

indiv = [('student','student'), ('enterpreneur','enterpreneur'), ('Businessman','Businessman'),('Employee','Employee')]
searching = [('startup-idea','startup-idea'), ('startup-company','startup-company')]
joinas = [('cofounder','cofounder'),('team-member','team-member'),('partner','partner'),('others','others')]
profas = [('student','student'), ('enterpreneur','enterpreneur'), ('Businessman','Businessman'),('Investor','Investor'),('Freelancers','Freelancers'),('Student Enterpreneur','Student Enterpreneur')]





class CompanyBase(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='CompanyUserProfile')
	logo=models.ImageField(upload_to='logo_pics',blank=True)
	brand_name=models.CharField(max_length=100,blank=False)
	company_name=models.CharField(max_length=100,blank=False)
	company_email=models.EmailField(blank=False)
	website=models.URLField()
	company_address=models.CharField(max_length=200,blank=False)
	city = models.CharField(max_length=200, blank=True)
	industry = models.CharField(max_length=100, blank=False)
	businesstype = models.CharField(max_length=200, blank=True)
	about_company=models.CharField(max_length=500,blank=False)
	created_at = models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return self.company_name






class Products(models.Model):
	productcompany = models.ForeignKey(CompanyBase,on_delete=models.CASCADE, unique=False,related_name='Product_cmp')
	product_pic = models.ImageField(upload_to='product_pics',blank=True)
	prod_name = models.CharField(max_length=200,blank=True)
	minimum_no = models.CharField(max_length=10,blank=False)
	price = models.CharField(max_length=5,blank=False)
	description = models.CharField(max_length=300,blank=True)

	def __str__(self):
		return self.prod_name




class EduDetails(models.Model):
	name = models.ForeignKey(User,on_delete=models.CASCADE,related_name='Edu_user')
	college_name = models.CharField(max_length=200,blank=True)
	course_name = models.CharField(max_length=200,blank=True)
	passing_year = models.DateTimeField()
	grade = models.IntegerField(default= 0)

	def __str__(self):
		return self.college_name



class SKILLS(models.Model):
	name = models.CharField(max_length=30)
	class Meta:
		ordering = ['name']
			
	def __str__(self):
		return self.name

class CofounderExperience(models.Model):
	ex_company_name=models.ForeignKey(CompanyBase,on_delete=models.CASCADE,related_name='Cofounder_experience_company')
	job_post=models.CharField(max_length=300,null=False,blank=False)
	starting_date=models.DateTimeField()
	ending_date=models.DateTimeField()
	def __str__(self):
		return self.job_post


class CofounderProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='Cofounder_user')
	im = models.CharField(max_length=100,blank=False,choices=profas) #edit
	looking_for = models.CharField(max_length=100,blank=False,choices=searching) #edit
	industry = models.CharField(max_length=200,blank=False)
	join_startup_as = models.CharField(max_length=100,blank=False,choices=joinas)
	workat = models.CharField(max_length=200,blank=True)
	education = models.ForeignKey(EduDetails,on_delete=models.CASCADE,related_name='Cofounder_edu',blank=True)
	skills = models.ManyToManyField(SKILLS,blank=False)
	experience = models.ManyToManyField(CofounderExperience,blank=True)
	aboutyourself = models.CharField(max_length=400, blank=True)
	created_at = models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return self.user.username


def create_profile(sender, **kwargs):
	if kwargs['created']:
		cofnd_profile = CofounderProfile.objects.create(user=kwargs['instance'])









jobtype = [('part_time','part_time'),('full_time','full_time'),('Freelancing_work','Freelancing_work'),('Internship','Internship')]

class JobOpening(models.Model):
	job_companyname = models.ForeignKey(CompanyBase,on_delete=models.CASCADE, unique=False,related_name='Company_details')
	jobtilte = models.CharField(max_length=200,blank=True,unique=True)
	location = models.CharField(max_length=200,blank=True)
	jobtype = models.CharField(max_length=100,blank=True,choices=jobtype)
	experience = models.CharField(max_length=80,blank=True)
	qualification = models.CharField(max_length=100,blank=False)
	last_date = models.DateTimeField()
	reqskills = models.ManyToManyField(SKILLS,blank=False)
	job_description=models.TextField(max_length=1000,blank=False)
	valid = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return self.jobtilte



selfchoices = [('Student','Student'),('Employee','Employee')]
class JobApplication(models.Model):
	jobtilte = models.ForeignKey(JobOpening,on_delete=models.CASCADE,related_name='Job_adding')
	applicant = models.ForeignKey(User,on_delete=models.CASCADE,related_name='applicant_details')
	applyas = models.CharField(max_length=100,blank=False,choices=selfchoices)
	college_name = models.CharField(max_length=200,blank=False)
	course_name = models.CharField(max_length=200,blank=False)
	passing_year = models.DateTimeField(blank=False)
	grade = models.IntegerField(default= 0,blank=False)
	resume = models.FileField(upload_to='resume',blank=False)
	aboutapplicant =  models.TextField(max_length=400,blank=False)
	def __str__(self):
		return self.applicant.username


class WorkProfile(models.Model):
	jobapplication = models.ForeignKey(JobApplication,on_delete=models.CASCADE,related_name='workprofile')
	Company_name =  models.CharField(max_length=200,blank=True)
	Post =  models.CharField(max_length=100,blank=True)
	Start_date = models.DateTimeField(blank=True)
	end_date = models.DateTimeField(blank=True)
	def __int__(self):
		return self.pk







categories = [('Business Advisor','Business Advisor'),
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
				('Hr','Hr')]






class FreelancersProfile(models.Model):
	theuser = models.OneToOneField(User,on_delete=models.CASCADE,related_name='FreelancerUserProfile')
	im = models.CharField(max_length=100,blank=False,choices=indiv)
	qualification =  models.CharField(max_length=100,blank=False)
	workingas =  models.CharField(max_length=100,blank=False,choices=categories)
	interestedin =  models.CharField(max_length=200,blank=False)
	lookingfor = models.CharField(max_length=200,blank=False)
	skills = models.ManyToManyField(SKILLS,blank=False)
	workpay = models.IntegerField(default= 0,blank=False)
	prevwork = models.CharField(max_length=200,blank=False)
	industry = models.CharField(max_length=100,blank=False)
	portfoliolink = models.URLField(max_length=200,blank=False)
	about = models.TextField(max_length=400,blank=False)
	def __str__(self):
		return self.theuser.username


internim = [('Intern','Intern'),('Employee','Employee'),('Job Seeker','Job Seeker')]
class InternProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='Intern_user')
	im = models.CharField(max_length=100, blank=False, choices=internim)
	work_at=models.CharField(max_length=100,blank=True)
	education = models.CharField(max_length=100,blank=False)
	skills = models.ManyToManyField(SKILLS, blank=False)
	experience = models.ManyToManyField(CofounderExperience,blank=True)
	about=models.CharField(max_length=300,blank=True)

	def __str__(self):
		return self.user.username


investorim = [('Individual Investor','Individual Investor'),('Angel Investor','Angel Investor'),('Venture Capitalist','Venture Capitalist'),('Investor Group','Investor Group')]

class InvestorProfile(models.Model):
	user= models.OneToOneField(User,on_delete=models.CASCADE,related_name='Investor_user')
	im=models.CharField(max_length=100, blank=False, choices=investorim)
	area_of_invest=models.CharField(max_length=100,blank=False)
	firm_name=models.CharField(max_length=100,blank=False)
	website=models.URLField()
	investment_location=models.CharField(max_length=100,blank=False)
	investment_range=models.CharField(max_length=20,blank=True)
	previous_investment=models.CharField(max_length=20,blank=True)
	about=models.CharField(max_length=200,blank=True)

	def __str__(self):
		return self.user.username







class LookingForFranchise(models.Model):
	investment = models.CharField(max_length=100, blank=True)
	space = models.CharField(max_length=100, blank=True)
	location = models.CharField(max_length=100, blank=True)
	industry = models.CharField(max_length=100, blank=False)
	product_or_services=models.CharField(max_length=100,blank=True)
	description = models.TextField(blank=False)
	industry_type = models.CharField(max_length=100, blank=False)
	business_nature = models.CharField(max_length=100, blank=False)
	about_comapny = models.TextField(blank=False)
	created_at = models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return self.industry


class Franchisor(models.Model):
	company_name = models.ForeignKey(CompanyBase,on_delete=models.CASCADE, unique=False,related_name='franchisor_company')
	providing=models.CharField(max_length=100,blank=False)
	brand_fee=models.CharField(max_length=10,blank=True)
	investment_req=models.CharField(max_length=100,blank=True)
	space_req=models.CharField(max_length=100,blank=True)
	staff_no=models.CharField(max_length=10,blank=True)
	monthly_sale=models.CharField(max_length=50,blank=False)
	profit=models.CharField(max_length=50,blank=True)
	royalties=models.CharField(max_length=20,blank=False)
	location=models.CharField(max_length=100,blank=True)
	description=models.TextField()
	product_view=models.ForeignKey(Products,on_delete=models.CASCADE, unique=False,related_name='franchisor_products')

	def __str__(self):
		return self.company_name



franchiseim = [('Franchisee','Franchisee'),('Distributor','Distributor'),('Wholesaler','Wholesaler')]
class Franchisee(models.Model):
	logo = models.ImageField(upload_to='logo_pics', blank=True)
	user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='Franchisee_user')
	comapny_name = models.ForeignKey(CompanyBase,on_delete=models.CASCADE, unique=False,related_name='franchisee_company')
	im = models.CharField(max_length=100, blank=False, choices=franchiseim)
	bussiness_email=models.EmailField(blank=False)
	website=models.URLField(blank=False)
	bussiness_address=models.TextField(max_length=300,blank=False)
	location = models.CharField(max_length=100, blank=True)
	industry_type = models.CharField(max_length=100, blank=False)
	companyyouworkfor=models.CharField(max_length=100,blank=True)
	about=models.TextField(blank=False)
	experience=models.TextField(blank=False)
	lookingforfranchise=models.ForeignKey(LookingForFranchise,on_delete=models.CASCADE, unique=False,related_name='franchisee_lookingfor')
	created_at = models.DateTimeField(auto_now_add= True)
	def __str__(self):
		return self.user



stage=[('Startup','Startup'),('MNC','MNC'),('Experianced','Experianced')]
class FundingPost(models.Model):
	company_name=models.ForeignKey(CompanyBase,on_delete=models.CASCADE, unique=False,related_name='Company_funding')
	lookingfor = models.CharField(max_length=200, blank=False)
	funding_required=models.CharField(max_length=10,blank=True)
	comapany_stage=models.CharField(max_length=100, blank=False, choices=stage)
	year_of_establish=models.DateField(blank=False)
	employee_No=models.CharField(max_length=5,blank=False)
	business_type=models.CharField(max_length=100,blank=False)
	business_description=models.CharField(max_length=100,blank=False)
	highlights=models.CharField(max_length=200,blank=True)
	annual_turnover=models.CharField(max_length=10,blank=True)
	growth_rate=models.CharField(max_length=100,blank=False)
	description=models.TextField()
	created_at = models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return self.company_name.company_name