from rest_framework import serializers
from forms.models import CompanyBase,Products,CofounderProfile,EduDetails,CofounderExperience,JobOpening,JobApplication,FreelancersProfile,SKILLS,FundingPost,Franchisee,WorkProfile,Franchisor,LookingForFranchise,InvestorProfile,InternProfile
#from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

User = get_user_model()


class CompanyBasesrializer(serializers.ModelSerializer):
	CompanyUser = serializers.CharField(source='user')
	CompanyUser_id = serializers.PrimaryKeyRelatedField(queryset= User.objects.all(),write_only=True)
	class Meta:
		model = CompanyBase
		fields = ['CompanyUser','CompanyUser_id','company_name','company_email','website','company_address','city','industry','businesstype','about_company']



class JobOpeningSerializer(serializers.ModelSerializer):
	company = serializers.CharField(source='ForCompany')
	class Meta:
		model = JobOpening
		fields = ['company','JobTilte','Location','JobType','experience','Last_date','reqskills','valid']



class JobApplicationSerializer(serializers.ModelSerializer):
	thejob = serializers.CharField(source='jobtilte')
	companyis = serializers.CharField(source='jobtilte.ForCompany')
	applicantis = serializers.CharField(source='applicant')
	class Meta:
		model = JobApplication
		fields = ['thejob','applicantis','companyis','applyas','college_name','course_name','passing_year','grade','resume','aboutapplicant']



class skillsserializers(serializers.ModelSerializer):
	class Meta:
		model: SKILLS

class FreelancersSerializer(serializers.ModelSerializer):
	useris = serializers.CharField(source='theuser')
	skills = serializers.SlugRelatedField(many=True, slug_field='name',queryset=SKILLS.objects.all())
	class Meta:
		model = FreelancersProfile
		fields = ['useris','im','qualification','workingas','interestedin','lookingfor','skills','workpay','prevwork','industry','portfoliolink','about']




class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model =EduDetails
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    productcompany = CompanyBasesrializer()
    class Meta:
        model =Products
        fields = '__all__'

class FranchiseeSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    comapny_name = CompanyBasesrializer()
    class Meta:
        model =Franchisee
        fields = '__all__'

class FranchisorSerializer(serializers.ModelSerializer):
    company_name = CompanyBasesrializer()
    product_view = ProductSerializer(many=False)
    class Meta:
        model =Franchisor
        fields = '__all__'

class LookingForFranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model =LookingForFranchise
        fields = '__all__'

class CofounderExperienceSerializer(serializers.ModelSerializer):
	ex_company_name = CompanyBasesrializer()
	class Meta:
		model =CofounderExperience
		fields = '__all__'


class InvestorSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    class Meta:
        model =InvestorProfile
        fields = '__all__'

class InternSerializer(serializers.ModelSerializer):
	user = serializers.CharField()
	skills = serializers.SlugRelatedField(many=True, slug_field='name',queryset=SKILLS.objects.all())
	experience = CofounderExperienceSerializer(many=True)
	class Meta:
		model =InternProfile
		fields = '__all__'


class CofounderSerializer(serializers.ModelSerializer):

	education = EducationSerializer(many=False)
	skills = serializers.SlugRelatedField(many=True, slug_field='name',queryset=SKILLS.objects.all())
	experience = CofounderExperienceSerializer(many=True)
	class Meta:
		model =CofounderProfile
		fields = ('user','im','looking_for','industry','experience','join_startup_as','workat','education','skills','aboutyourself','created_at')

class WorkProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =WorkProfile
        fields = '__all__'

class FundingSerializers(serializers.ModelSerializer):
    company_name = CompanyBasesrializer(many=False)
    class Meta:
        model =FundingPost
        fields = '__all__'

