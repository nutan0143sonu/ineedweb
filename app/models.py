import jwt
import uuid
import pyotp

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin

from rest_framework_jwt.utils import jwt_payload_handler
from cloudinary.models import CloudinaryField
from djrichtextfield.models import RichTextField

from .utils import *



#---------------------------------------PROFESSION-----------------------------------#


class Profession(models.Model):
    name = models.CharField(
        "Profession",max_length = 50,
        blank = True,null = True)
    
    def __str__(self):
        return str(self.name)

#-------------------------Language Coversion Table--------------------------------------
class LanguageTranslation(models.Model):
    language = models.CharField(
        "Language Name",
        max_length=100
    )
    key = models.CharField(
        "Language Key",
        max_length =30
    )
    def __str__(self):
        return self.language
    
    class Meta:
        verbose_name_plural="Language Translation Key"
#-------------------------Industy Model-------------------------------------------------

class IndustryModel(models.Model):
    """Industry Model """
    industry_type = models.CharField(
        "Industry Type", max_length=60
    )

    def __str__(self):
        """code + Industry Type"""
        return "%s" % (self.industry_type)

#-----------------------------Area Model------------------------------

class AreaModel(models.Model):
    """Area Model"""
    area = models.CharField(
        "Area", max_length=50
    )

    def __str__(self):
        """code + Area"""
        return "%s" % (self.area)

#--------------Tools And Language Model---------------------------------

class ToolsAndLanguageModel(models.Model):
    """Tools And Language Model"""
    name = models.CharField(
        "Tools and Language", max_length=50
    )

    def __str__(self):
        """code + Tools or language"""
        return "%s" % (self.name)

#-------------Laguage Model------------------------------
class SpeakingLanguageModel(models.Model):
    """Language Model"""
    language_name = models.CharField(
        "Language Name",
        max_length=40
    )

    def __str__(self):
        """code + Language"""
        return "%s" % (self.language_name)

#-------------Working Hour Model--------------------------
class WorkingHourModel(models.Model):
    """Working Hour Model"""
    working_hour = models.CharField(
        "Working Hour in a Week",
        max_length=15
    )
    def __str__(self):
        """code + Working Hour"""
        return "%s" % (self.working_hour)
#-------------MyUserManger Model -------------------------
class MyUserManager(BaseUserManager):
    '''Inherits BaseUserManager Class'''

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        print("email", email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        print("user", user)
        return user

    # def create_user(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_superuser', False)
    #     print("Useris created")
    #     return self._create_user(email, password, **extra_fields)

    def create_superuser(self,email,password):
        '''Create and saves a superuser with the given email and password '''
        user=self.model(email=email)
        user.set_password(password)
        user.is_superuser=True
        user.is_active=True
        user.is_staff=True
        user.save(using=self._db)
        return user


#------------MyUser Model-------------------------------------
class MyUser(AbstractBaseUser, PermissionsMixin):
    '''Base User Table used same for Authentication Purpose'''
    '''Docstribg for MyUser'''
    USERTYPE = (
        ("Job Seeker", "Job Seeker"),
        ("Company", "Company"),
    )


    uuid = models.UUIDField(
        'UUID', default=uuid.uuid4, editable=False, unique=True
    )
    email = models.EmailField(
        "Email", unique=True, max_length=50, validators=[EMAILREGEX]
    )
    first_name = models.CharField(
        "First Name", max_length=40, validators=[NAMEREGEX], blank=True, null=True
    )
    last_name = models.CharField(
        "Last Name", max_length=40, validators=[NAMEREGEX],  blank=True, null=True
    )
    user_type = models.CharField(
        "User Type", max_length=20, default='Job Seeker', choices= USERTYPE
    )
    otp = models.CharField(
        "OTP", blank=True, null=True, max_length=7
    )

    is_active = models.BooleanField(
        'Active', default=False
    )
    is_staff = models.BooleanField(
        'Staff',default=False
    )
    image = models.URLField(
        'image',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects=MyUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        """code + User email"""
        return "%s" % (self.email)
    

    def get_short_name(self):
        return self.first_name

    def otp_verify(self):
        totp = pyotp.TOTP("JBSWY3DPEHPK3PXP")
        print(totp.now())
        self.otp=totp.now()
        self.save()
        return self.otp

    def send_mail1(self):
        subject="Otp For Your Email Verification"
        message="The OTP is "+str(self.otp)
        send_mail(subject,message,'nutan110125@gmail.com',[self.email],fail_silently=False)
        return self.email

    def create_jwt(self):
        """Function for creating JWT for Authentication Purpose"""
        payload = jwt_payload_handler(self)
        token = jwt.encode(payload, settings.SECRET_KEY)
        auth_token = token.decode('unicode_escape')
        return auth_token


    class Meta:
        '''docstring for Meta'''
        verbose_name_plural="User"
        
    def get_short_name(self):
        return self.first_name
#---------------------User or Company Industry Model---------------------------------------
class UserIndustryModel(models.Model):
    """User Industry Data"""
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name= 'user_industry'
    )
    industry = models.ForeignKey(
        IndustryModel,
        on_delete = models.CASCADE ,
        related_name='industry_name'
    )

    def __str__(self):
        """code + User email"""
        return "%s" % (self.industry)



#----------------------User Area Model-------------------------------------------
class UserAreaModel(models.Model):
    """User Area Data"""
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='user_area'
    )
    area = models.ForeignKey(
        AreaModel,
        on_delete = models.CASCADE,
        related_name='area_name'
    )

    def __str__(self):
        """code + User email"""
        return "%s" % (self.area)

#---------------------User Tools And Language Data------------------------------
class UserToolsAndLanguageModel(models.Model):
    """User Tools and Language Model"""
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='user_skill'
    )
    skill =  models.ForeignKey(
        ToolsAndLanguageModel,
        on_delete = models.CASCADE,
        related_name='skill_name'
    )

    rating = models.IntegerField(
        "Rating of Skill",
        blank=True,
        null=True,
        default=0
    )
    def __str__(self):
        """code + User email"""
        return "%s" % (self.skill)

#---------------------personal Detail Model-------------------------------------
class PersonalDetailModel(models.Model):
    """User Profestional data"""
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        related_name='user_personal_detail'
    )
    work_hour = models.ForeignKey(
        WorkingHourModel,
        on_delete=models.CASCADE,
        related_name="user_working_hour_in_a_week",
        blank=True,
        null=True
    )
    professional_title = models.CharField(
        "Profestional Title",
        max_length=100,
        blank=True,
        null=True
    )
    professional_description = models.TextField(
        "Professional Description",
        blank=True,
        null=True
    )
    paypal_account_id = models.CharField(
        "Paypal Account Id",
        max_length=65,
        blank=True,
        null=True
    )
    #personal data
    country = models.CharField(
        "Country Name",
        max_length=40,
        blank=True,
        null=True
    )
    timezone = models.CharField(
        "Timezone",
        max_length=20,
        blank=True,
        null=True
    )
    postal_code = models.CharField(
        "Postal Vode",
        blank=True,
        null=True,
        max_length=10
    )
    city = models.CharField(
        "city",
        max_length=50,
        blank=True,
        null=True,
        validators=[NAMEREGEX]
    )
    mobile = models.CharField(
        "Phone Number",
        max_length=18,
        blank=True,
        null=True,
        validators=[MOBILEREGEX]
    )

    def __str__(self):
        """code + User email"""
        return "%s" % (self.professional_title)


#-----------------User Language Model------------------------------------------------------
class UserLanguageModel(models.Model):
    """Job seeker language Model"""
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="user_language"
    )
    userLanguage = models.ForeignKey(
        SpeakingLanguageModel,
        on_delete=models.CASCADE,
        related_name="user_language_name"
    )
    rating = models.IntegerField(
        "Language Rating",
        default=0
    )

    def __str__(self):
        """code + User email"""
        return "%s" % (self.userLanguage)


#-----------------------------User Education Model---------------------------------------------
class UserEducationModel(models.Model):
    """Jobseeker Education History Model"""
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='user_education'
    )
    schoolName = models.CharField(
        "School or Collage Name",
        max_length=250,
        blank=True,
        null=True
    )
    university_name = models.CharField(
        "University name",
        max_length=100,
        blank=True,
        null=True
    )
    board = models.CharField(
        "Boards",
        max_length=40,
        blank=True,
        null=True
    )
    percentage = models.FloatField(
        "percentage",
        blank=True,
        null=True
    )
    yos = models.CharField(
        "Year Of Starting",
        max_length=10,
        blank=True,
        null=True,validators=[YEARREGEX]
    )
    yop = models.CharField(
        "Year Of Passing",
        max_length=10,
        blank=True,
        null=True,validators=[YEARREGEX]
    )
    course = models.CharField(
        "Course",
        max_length=50,
        blank=True,
        null=True
    )
    stream = models.CharField(
        "Stream",
        max_length=40,
        blank=True,
        null=True
    )
    activity = RichTextField(
        "Activities and societies",
        blank=True,
        null=True
    )
    description =RichTextField(
        "Description",
        blank=True,
        null=True
    )
    def __str__(self):
        """code + User email"""
        return "%s" % (self.schoolName)
#----------------Employment History Model-------------------------------------------------------
class UserEmploymentHistoryModel(models.Model):
    """Jobseeker Employement History Models"""
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='user_employment'
    )
    company_name = models.CharField(
        "company name",
        max_length=50,
        blank=True,
        null=True
    )
    designation = models.CharField(
        "Designation",
        max_length=30,
        blank=True,
        null=True
    )
    fromMonth = models.CharField(
        "From Month ",
        max_length=15,
        validators=[NAMEREGEX]
    )
    fromYear = models.CharField(
        "Frrom Year",
        max_length=5,
        validators=[YEARREGEX]
    )
    toMonth = models.CharField(
        "To Month",
        max_length=15,
        blank=True,
        null=True,
        validators=[NAMEREGEX]
    )
    toYear = models.CharField(
        "To Year",
        max_length=5,
        validators=[YEARREGEX],
        blank=True,
        null=True
    )
    currentWorking = models.BooleanField(
        "Current Working",
        default=False
    )
    city = models.CharField(
        "City of Company",
        max_length=40,
        blank=True,
        null=True,
        validators=[NAMEREGEX]
    )
    country = models.CharField(
        "Country of Comapany",
        max_length=40,
        blank=True,
        null=True,
        validators=[NAMEREGEX]
    )
    jobDescription = models.TextField(
        "Description of Job",
        blank=True,
        null=True,
    )

    def __str__(self):
        """code + User email"""
        return "%s" % (self.company_name)

