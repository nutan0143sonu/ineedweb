from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from django.utils.functional import lazy, SimpleLazyObject

from .translations import *
from .models import *
from app.models import *

#------------Industry Serializer---------------------
class IndustrySerializer(serializers.ModelSerializer):
    """Industry Serializer for getting all data of industry."""
    class Meta:
        model = IndustryModel
        fields = '__all__'
#---------------Area serializer----------------------
class AreaSerializer(serializers.ModelSerializer):
    """Area Serializer for getting all data of area."""
    class Meta:
        model = AreaModel
        fields = '__all__'
#---------------Tool and
class ToolsAndLanguageSerializer(serializers.ModelSerializer):
    """Skill Serializer for getting all data of tools and language"""
    class Meta:
        model = ToolsAndLanguageModel
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    """Login Serializer"""
    class Meta:
        model = MyUser
        fields =  ('email',)



class UserAreaSerializer(serializers.ModelSerializer):
    """Job seeker Area Serializer"""
    area_name = AreaSerializer(read_only=True, many=True)
    name = SerializerMethodField()

    def get_name(self,obj):
        if obj.area:
            return obj.area.area
    class Meta:
        model = UserAreaModel
        exclude = ('user','area')

class UserIndustrySerializer(serializers.ModelSerializer):
    """Job seeker Industry Serializer"""
    industry_name = IndustrySerializer(read_only=True, many=True)
    name = SerializerMethodField()

    def get_name(self, obj):
        if obj.industry:
            return obj.industry.industry_type

    class Meta:
        model = UserIndustryModel
        exclude = ('user','industry',)


class UserToolAndLanguageserializer(serializers.ModelSerializer):
    """Job Seeker Skills Serializer"""
    skill_name = ToolsAndLanguageSerializer(read_only=True, many=True)
    name = SerializerMethodField()

    def get_name(self, obj):
        if obj.skill:
            return obj.skill.name
    class Meta:
        model = UserToolsAndLanguageModel
        exclude = ('user','skill',)


class UserSignupSerializers(serializers.ModelSerializer):
    """Job Seeker Signup Serlaizer"""
    def create(self, validated_data):
        params = self.context.get('params')
        user = MyUser.objects.create(**validated_data)
        user.set_password(params['password'])
        user.save()

        if 'industry' in params:
            for data in params['industry']:
                try:
                    industry = IndustryModel.objects.get(id=data)
                    obj, created = UserIndustryModel.objects.get_or_create(user=user, industry=industry)
                    obj.save()
                except:
                    pass
        if 'area' in params:
            for data in params['area']:
                try:
                    area = AreaModel.objects.get(id=data)
                    obj, created = UserAreaModel.objects.get_or_create(user=user, area=area)
                    obj.save()
                except:
                    pass

        if 'tool_and_language' in params:
            for key,data in params['tool_and_language'].items():
                try:
                    skill = ToolsAndLanguageModel.objects.get(id=key)
                    obj, created = UserToolsAndLanguageModel.objects.get_or_create(user=user, skill=skill)
                    obj.rating = data
                    obj.save()
                except:
                    pass

        PersonalDetailModel.objects.create(user=user,**params['personal'])
        return user


    class Meta:
        model = MyUser
        fields = "__all__"

#------------------------Edit Profile Serializer----------------
class UserEditProfileSerializer(serializers.ModelSerializer):
    """Serializer for editing job seeker profile."""
    class Meta:
        model = MyUser
        fields = '__all__'

#-----------------Image Upload Serializer----------------------
class ImageUploadserializer(serializers.ModelSerializer):
    """Serilazer for Image upload."""
    class Meta:
        model = MyUser
        fields = ('image',)


#----------------Working Hour Serializer-------------------------
class WorkingHourSerializer(serializers.ModelSerializer):
    """Serializer for working hour"""
    class Meta:
        model = WorkingHourModel
        fields = '__all__'
#-------------------persional detail--------------------------
class UserpersonalDetailSerializer(serializers.ModelSerializer):
    """serializer of jobseeker persional detal"""
    user_working_hour_in_a_week  = WorkingHourSerializer(read_only=True, many=True)
    work_hour = SerializerMethodField()

    def get_work_hour(self, obj):
        if obj.work_hour:
            return obj.work_hour.working_hour

    class Meta:
        model = PersonalDetailModel
        exclude = ('user','id')
#-----------------------------User Education Serializer--------------------------------------
class UserEducationSerializer(serializers.ModelSerializer):
    """Serilizer for user Education"""
    class Meta:
        model = UserEducationModel
        fields = '__all__'

#----------------Availability and location serializer-----------
class AvailabilityAndLocationSerializer(serializers.ModelSerializer):
    """Serializer of Availability and Locality of job seeker"""
    class Meta:
        model = PersonalDetailModel
        fields = '__all__'

#----------------Language Serializer------------------------------
class SpeakingLanguageSerializer(serializers.ModelSerializer):
    """Speaking Language serializer"""
    class Meta:
        model = SpeakingLanguageModel
        fields = '__all__'

#------------------User Speaking Language---------------------------
class UserSpeakingLanguage(serializers.ModelSerializer):
    """Job Seeker Speaking Laguage Serializer"""
    lang = SerializerMethodField()

    def get_lang(self,obj):
        if obj.userLanguage:
            return obj.userLanguage.language_name
    class Meta:
        model = UserLanguageModel
        exclude = ('user','id')
#----------------Salary-----------------------------------------------
class SalarySerializer(serializers.ModelSerializer):
    """Salary Serializer"""
    class Meta:
        model = Salary
        fields = '__all__'   

#-------------------Location--------------------------------------------
class LocationSerializer(serializers.ModelSerializer):
    """Location Serializer"""
    class Meta:
        model = Location
        fields = '__all__'  

#-----------------------------Employment History Serializer-------------------------------
class EmploymentHistorySerializer(serializers.ModelSerializer):
    """Job Seeker Employement Serializer"""
    class Meta:
        model = UserEmploymentHistoryModel
        fields = "__all__"


#--------- Profile complete Serializer-------------------------------------
class UserSerializer(serializers.ModelSerializer):
    """Job Seeker Serializer"""
    user_industry = UserIndustrySerializer(read_only=True, many=True)
    user_area = UserAreaSerializer(read_only=True, many=True)
    user_personal_detail = UserpersonalDetailSerializer(read_only=True)
    user_skill = UserToolAndLanguageserializer(read_only=True, many=True)
    user_language = UserSpeakingLanguage(read_only=True, many=True)
    user_education = UserEducationSerializer(many=True)
    user_employment = EmploymentHistorySerializer(many=True)

    class Meta:
        model = MyUser
        exclude = ('password','last_login','is_superuser','uuid','is_active',
                   'is_staff','created_at','updated_at','user_permissions','groups','otp')


#------------------------------------EmployerSignUp--------------------#

class EmployerSignupSerializers(serializers.ModelSerializer):
    """Company Signup Serilaizer"""
    def create(self, validated_data):
        params = self.context.get('params')
        user = MyUser.objects.create(**validated_data)
        user.set_password(params['password'])
        user.save()
        for data in params['industry_type']:
            print("data",data)
            industry,create = IndustryModel.objects.get_or_create(industry_type=data)
            print("industry",industry.id)
            created = UserIndustryModel.objects.create(user=user, industry=industry)
        return user
    class Meta:
        model = MyUser
        fields = "__all__"

#----------------------------Notification-----------------------------------------
class NotificationSerializer(serializers.ModelSerializer):
    """Notification Serializer"""
    class Meta:
        model = Notification
        fields = "__all__"

#--------------------------------Post Job Serializer----------------------------------------#
class PostJobStep2serailizer(serializers.ModelSerializer):
    """Post job step2 serializer"""
    class Meta:
        model = JobManagement
        fields = "__all__"


#------------------------Edit Posted Job Serializer Step1-----------------------------------
class EditPostedJobStep1Serializer(serializers.ModelSerializer):
    """EDIT JOB  step1 serializer"""
    def update(self,instance,validated_data):
        params = self.context.get('params')
        instance.jobTitle = validated_data.get('jobTitle',params['jobTitle'])
        instance.jobDiscription = validated_data.get('jobDiscription',params['jobDiscription'])
        delPostedarea = PostJobAreaModel.objects.filter(job=instance).delete()
        for data in params['area']:
            workArea,create = AreaModel.objects.get_or_create(area=data)
            PostJobAreaModel.objects.create(job=instance,area=workArea)  
        instance.save()
        return instance

    class Meta:
        model = JobManagement
        fields = "__all__"


#-----------------------Posted job Serializer------------------------------------------------
class PostedJobArea(serializers.ModelSerializer):
    """Posted job area serializer"""
    area = SerializerMethodField()

    def get_area(self,obj):
        if obj.area:
            return obj.area.area
    
    class Meta:
        model = PostJobAreaModel
        fields = ('id','area',)

class PostSkillSerilizer(serializers.ModelSerializer):
    """Post job skill serializer"""
    skills = SerializerMethodField()
    
    def get_skills(self,obj):
        if obj.skills:
            return obj.skills.name
        
    class Meta:
        model = PostJobSkillModel
        fields = ('id','skills')

class PostJoblanguageSerializer(serializers.ModelSerializer):
    """posted job language serializer"""
    language = SerializerMethodField()

    def get_language(self,obj):
        if obj.preferenceLanguage:
            return obj.preferenceLanguage.language_name

    class Meta:
        model = PostJobPreferenceLanguageModel
        fields = ('id','language')

class PostJobLocationSerializer(serializers.ModelSerializer):
    """Posted job location serializer"""
    location = SerializerMethodField()
    
    def get_location(self,obj):
        if obj.preferenceLocation:
            return obj.preferenceLocation.locationName

    class Meta:
        model = PostJobPreferenceLocationModel
        fields = ('id','location') 

class EmployerPostedJobSerializer(serializers.ModelSerializer):
    """Company Posted job serializer"""
    post_job_area = PostedJobArea(many=True)
    post_job_skill = PostSkillSerilizer(many=True)
    post_job_preference_language = PostJoblanguageSerializer(many=True)
    post_job_preference_location = PostJobLocationSerializer(many=True)
    salary = SerializerMethodField()
    employer = SerializerMethodField()
    image = SerializerMethodField()
    def get_salary(self,obj):
        if obj.desiredSalary:
            return obj.desiredSalary.salaryPerHour
    
    def get_employer(self,obj):
        if obj.user:
            return obj.user.first_name
    def get_image(self,obj):
        if obj.user:
            return obj.user.image
    
    class Meta:
        model = JobManagement
        fields = "__all__"


#------------------Employer Profile--------------------------------------------------------------------
class EmployerProfileSerializer(serializers.ModelSerializer):
    """Company profile Serializer"""
    user_industry = UserIndustrySerializer(read_only=True, many=True)
    class Meta:
        model = MyUser
        fields = '__all__'

#----------------------Get User Education Serializer--------------------------------------
class GetUserEducationSerializer(serializers.ModelSerializer):
    """Job seeker education serializer"""
    class Meta:
        model = UserEducationModel
        fields = '__all__'  

class UserDetail(serializers.ModelSerializer):


    class Meta:
        model = MyUser
        fields = ("id","email","first_name","last_name","image")

class ReviewAndRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewAndRating
        fields = "__all__"   
                          
#----------------------Get User Education Serializer--------------------------------------
class GetUserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducationModel
        fields = '__all__'  

#--------------Job Seeker Job Serializer---------------------------------------------------
def user(user,data):
    data = UserApplyJob.objects.get(user=request.user,job__id__in=data)
    return data
class JobSeekerjobSerailizer(serializers.ModelSerializer):
    post_job_area = PostedJobArea(many=True)
    post_job_skill = PostSkillSerilizer(many=True)
    post_job_preference_language = PostJoblanguageSerializer(many=True)
    post_job_preference_location = PostJobLocationSerializer(many=True)
    salary = SerializerMethodField()
    employer = SerializerMethodField()
    image = SerializerMethodField()
    is_applied = SerializerMethodField()
    is_favourite= SerializerMethodField()
    is_approved = SerializerMethodField()
    user_applied_job_id = SerializerMethodField()
    def get_user_applied_job_id(self,obj):
        applied_job_id = self.context.get('applied_job')
        user = self.context.get('user')
        if obj.id in applied_job_id:
            return user.user_favourite.get(user=user,job__id=obj.id).id

    def get_is_applied(self,obj):
        applied_job_id = self.context.get('applied_job')
        user = self.context.get('user')
        if obj.id in applied_job_id:
            return user.user_favourite.get(user=user,job__id=obj.id).is_apply

    def get_is_favourite(self,obj):
        applied_job_id = self.context.get('applied_job')
        user = self.context.get('user')
        if obj.id in applied_job_id:
            return user.user_favourite.get(user=user,job__id=obj.id).is_favourite
       
    def get_is_approved(self,obj):
        applied_job_id = self.context.get('applied_job')
        user = self.context.get('user')
        if obj.id in applied_job_id:
            return user.user_favourite.get(user=user,job__id=obj.id).is_approved

    def get_salary(self,obj):
        if obj.desiredSalary:
            return obj.desiredSalary.salaryPerHour
        
    def get_employer(self,obj):
        if obj.user:
            return obj.user.first_name
    def get_image(self,obj):
        if obj.user:
            return obj.user.image
    

    class Meta:
        model = JobManagement
        fields = "__all__"

class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApplyJob
        fields = "__all__"

#---------------------------User Apply job notification-------------
class UserApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApplyJob
        fields =("resume","hire_question")
#--------------Contact Us for Websit Post Api-----------------------
class PostContactUsSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields="__all__"



class JobSeekerComletedJobSerializer(serializers.ModelSerializer):
    post_job_area = PostedJobArea(many=True)
    post_job_skill = PostSkillSerilizer(many=True)
    post_job_preference_language = PostJoblanguageSerializer(many=True)
    post_job_preference_location = PostJobLocationSerializer(many=True)
    salary = SerializerMethodField()
    employer = SerializerMethodField()
    image = SerializerMethodField()
    job_seeker_is_completed = SerializerMethodField()
    is_favourite= SerializerMethodField()
    employer_is_completed = SerializerMethodField()
    is_applied = SerializerMethodField()
    is_approved = SerializerMethodField()
    company_rating = SerializerMethodField()
    company_review = SerializerMethodField()
    
    def get_job_seeker_is_completed(self,obj):
        applied_job_id = self.context.get('applied_job')
        user = self.context.get('user')
        if obj.id in applied_job_id:
            return user.user_favourite.get(user=user,job__id=obj.id).job_seeker_is_completed

    def get_is_favourite(self,obj):
        applied_job_id = self.context.get('applied_job')
        user = self.context.get('user')
        if obj.id in applied_job_id:
            return user.user_favourite.get(user=user,job__id=obj.id).is_favourite
       
    def get_employer_is_completed(self,obj):
        applied_job_id = self.context.get('applied_job')
        user = self.context.get('user')
        if obj.id in applied_job_id:
            return user.user_favourite.get(user=user,job__id=obj.id).employer_is_completed
    def get_is_applied(self,obj):
        applied_job_id = self.context.get('applied_job')
        user = self.context.get('user')
        if obj.id in applied_job_id:
            return user.user_favourite.get(user=user,job__id=obj.id).is_apply
       
    def get_is_approved (self,obj):
        applied_job_id = self.context.get('applied_job')
        user = self.context.get('user')
        if obj.id in applied_job_id:
            return user.user_favourite.get(user=user,job__id=obj.id). is_approved 
    def get_salary(self,obj):
        if obj.desiredSalary:
            return obj.desiredSalary.salaryPerHour
    def get_employer(self,obj):
        if obj.user:
            return obj.user.first_name
    def get_image(self,obj):
        if obj.user:
            return obj.user.image

    def get_company_rating(self,obj):
         applied_job_id = self.context.get('applied_job')
         user = self.context.get('user')
         if obj.id in applied_job_id:
             data = user.user_favourite.get(user=user,job__id=obj.id)
             return ReviewAndRating.objects.get(receiver_user=data.job.user,applied_job=data).rating
    def get_company_review(self,obj):
         applied_job_id = self.context.get('applied_job')
         user = self.context.get('user')
         if obj.id in applied_job_id:
             data = user.user_favourite.get(user=user,job__id=obj.id)
             return ReviewAndRating.objects.get(receiver_user=data.job.user,applied_job=data).review

    class Meta:
        model = JobManagement
        fields = "__all__"

#--------------------------------Employer Active Job Serializer------------------------
class EmployerActiveJobSerializer(serializers.ModelSerializer):
    job_detail = EmployerPostedJobSerializer(source='job')
    user_detail = UserSerializer(source='user')

    class Meta:
        model = UserApplyJob
        fields = ('id','is_apply','is_approved','is_accepted','job_seeker_is_completed','user_detail','job_detail')

#----------------------------Employer Completed Job Serializer--------------------
class EmployerCompletedJobSerializer(serializers.ModelSerializer):
    job_detail = EmployerPostedJobSerializer(source='job')
    user_detail = UserSerializer(source='user')
    jobseeker_review = SerializerMethodField()
    jobseeker_rating = SerializerMethodField()
    def get_jobseeker_rating(self,obj):
        if obj:
            return ReviewAndRating.objects.get(receiver_user=obj.user,applied_job__id=obj.id).rating
        
    def get_jobseeker_review(self,obj):
        return ReviewAndRating.objects.get(receiver_user=obj.user,applied_job__id=obj.id).review
    
    class Meta:
        model = UserApplyJob
        fields = ('id','is_apply','is_approved','is_accepted','job_seeker_is_completed','jobseeker_rating','jobseeker_review','user_detail','job_detail')

#--------------------------top 10 company Serailizer---------------------------------------------------
class Top10CompanySerializer(serializers.ModelSerializer):
    applicant = SerializerMethodField()
    place = SerializerMethodField()
    def get_applicant(self,obj):
        if obj:
            user=UserApplyJob.objects.filter(job__user__id=obj.id).distinct('user')
            return user.count()
    def get_place(self,obj):
        return "Multiple Place"
    class Meta:
        model = MyUser
        fields = ('first_name','image','applicant','place')


#--------------------------top 10 Jobseeker Serailizer---------------------------------------------------
class Top10JobSeekerSerializer(serializers.ModelSerializer):
    user_personal_detail = UserpersonalDetailSerializer(read_only=True)
    place = SerializerMethodField()
    def get_title(self,obj):
        if obj:
            return obj.professional_title
    def get_place(self,obj):
        return "Not To disclose"
    class Meta:
        model = MyUser
        fields = ('first_name','image','user_personal_detail','place')


class UserTestingSerializer(serializers.ModelSerializer):
    # user_employment = EmploymentHistorySerializer(many=True)

    industry = SerializerMethodField()
    area = SerializerMethodField()
    personal = SerializerMethodField()
    skill = SerializerMethodField()
    language = SerializerMethodField()
    education = SerializerMethodField()
    def get_industry(self,obj):
        data = industryTranslation(obj,language='fr')
        return data
    def get_area(self,obj):
        data = areaTranslation(obj,language='fr')
        return data
    def get_personal(self,obj):
        data = personalDetailTranslation(obj,language='fr')
        return data
    def get_skill(self,obj):
        data = skillTranslation(obj,language='fr')
        return data
    def get_language(self,obj):
        data = languageTranslation(obj,language='fr')
        return data
    def get_education(self,obj):
        data = languageTranslation(obj,language='fr')
        return data

    class Meta:
        model = MyUser
        exclude = ('password','last_login','is_superuser','uuid','is_active',
                   'is_staff','created_at','updated_at','user_permissions','groups','otp')

#------------------------------Chat Serializer--------------------------
class ChatSerializer(serializers.ModelSerializer):
    sender = SerializerMethodField()
    receiver = SerializerMethodField()
    def get_sender(self,obj):
        if obj.sender:
            return obj.sender.first_name
    def get_receiver(self,obj):
        if obj.receiver:
            return obj.receiver.first_name
    class Meta:
        model = ChatModel
        fields = "__all__"