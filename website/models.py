import uuid

from app.models import *
from django.db import models
from datetime import datetime
from djrichtextfield.models import RichTextField

#------------------Location Model--------------------------------------------------------
class Location(models.Model):
    """Model for location of posted job."""
    locationName = models.CharField("Location",max_length=100)
    
    def __str__(self):
        return self.locationName

    class Meta:
        verbose_name_plural = "Location Name" 

#------------------Salary Model--------------------------------------------------------
class Salary(models.Model):
    """Model creation for salary"""
    salaryPerHour = models.CharField("Salary Per Hour",max_length=100)
    
    def __str__(self):
        return self.salaryPerHour

    class Meta:
        verbose_name_plural = "Salary Per Hour" 


#---------------------Post Job Management--------------------------------------------------
class JobManagement(models.Model):
    """Model Creation for posting job."""
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="company",
        blank=True,
        null=True
    )
    jobTitle = models.CharField(
        "Job Title",
        max_length=100
         )
    jobDiscription = RichTextField("Job Description")
    requiredAnalytics = models.IntegerField("Number of Employee",blank=True,null=True)
    approved_employee = models.IntegerField("Number of approvd employee",default=0)
    TYPE_OF_PROJECT = (
        ("One Time Project", "One Time Project"),
        ("On going Project", "On going Project"),
        ("To be decided", "To be decided")
    )
    type_of_project = models.CharField(
        "What type of project you have?", default="One Time Project", max_length=50, choices=TYPE_OF_PROJECT
    )
    PAYMENT = (
        ("Pay by Hour", "Pay by Hour"),
        ("Pay by Fixed Price", "Pay by Fixed Price")
    )
    payment = models.CharField(
        "How would you like to pay?", default="Pay by Hour", max_length=50, choices=PAYMENT)
    DURATION_PROJECT = (
        ("0-3", "0-3"),
        ("3-6", "3-6"),
        ("6-12", "6-12"),
        ("12+", "12+"),
    )
    desiredSalary = models.ForeignKey(
        Salary,
        on_delete=models.CASCADE,
        related_name="salary_per_hour",
        blank=True,null=True
    )
    duration = models.CharField(
        "Month", max_length=10, default="0-3", choices=DURATION_PROJECT)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )

    def __str__(self):
        return self.jobTitle

# #-------------------------Post Job Area of Work----------------------------
class PostJobAreaModel(models.Model):
    """Model creation for post job area."""
    job = models.ForeignKey(
        JobManagement,
        on_delete=models.CASCADE,
        related_name="post_job_area"
    )
    area = models.ForeignKey(
        AreaModel,
        on_delete=models.CASCADE,
        related_name="post_job_area_of_work"
    )

    def __str__(self):

        return self.job.jobTitle

#-----------------Post job Tools And Language-----------------------------------
class PostJobSkillModel(models.Model):
    """Posted job skill Model"""
    job = models.ForeignKey(
        JobManagement,
        on_delete=models.CASCADE,
        related_name="post_job_skill"
    )
    skills = models.ForeignKey(
        ToolsAndLanguageModel,
         on_delete=models.CASCADE,
        related_name="skills_required"
    )
    def __str__(self):
        return self.job.jobTitle

#------------------------Post Job Preference Language----------------------------
class PostJobPreferenceLanguageModel(models.Model):
    """Posted job preference languag Model"""
    job = models.ForeignKey(
        JobManagement,
        on_delete=models.CASCADE,
        related_name="post_job_preference_language"
    )
    preferenceLanguage = models.ForeignKey(
        SpeakingLanguageModel,
        on_delete=models.CASCADE,
        related_name = "preference_language"
    )
    def __str__(self):
        return self.job.jobTitle

#-------------------------------Post Job Location-------------------------------------
class PostJobPreferenceLocationModel(models.Model):
    """Posted job of preference Location Model"""
    job = models.ForeignKey(
        JobManagement,
        on_delete=models.CASCADE,
        related_name="post_job_preference_location"
    )
    preferenceLocation  = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name = "preference_Location"
    )
    def __str__(self):
        return self.job.jobTitle

#-----------------------------------Favourite Job--------------------------------------------
class UserApplyJob(models.Model):
    """Jobseeker Apply job Model"""
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='user_favourite',
    )
    job = models.ForeignKey(
        JobManagement,
        on_delete=models.CASCADE,
        related_name="company_job",
    )
    hire_question = RichTextField("why_should_we_hire_you", blank=True, null=True)
    resume = models.URLField(
        "user_resume",
        blank = True,
        null=True
    )
    is_favourite = models.BooleanField(default=False)
    is_apply = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    job_seeker_is_completed  = models.BooleanField(default=False)
    employer_is_completed  = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural="User Apply Job"

#----------------------------------------Message or Chat Model----------------------------------------------
class ChatModel(models.Model):
    """Chat History Model"""
    sender = models.ForeignKey(
        MyUser,
        on_delete = models.CASCADE,
        related_name = "message_sender"
    )
    receiver = models.ForeignKey(
        MyUser,
        on_delete = models.CASCADE,
        related_name = "message_receiver"
    )
    accepted_applied_job = models.ForeignKey(
        UserApplyJob,
        on_delete = models.CASCADE,
        related_name = "user_applied_job"
    )
    message = models.TextField(
        "Employer or Job_seeker Message",
        blank=True,
        null = True
    )
    is_attachment = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField( "Created Date", auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return "{} {}".format(self.sender.first_name, self.sender.last_name)

    class Meta:
        verbose_name_plural = "Chat"

#-------------------Notification Model----------------------------------------------------
class Notification(models.Model):
    """Notifiaction Model for both Jobseeker and Company"""
    sender = models.ForeignKey(
     MyUser,
     on_delete=models.CASCADE,
     related_name= 'sender_notifcation',
     blank=True,
     null=True
    )
    receiver = models.ForeignKey(
     MyUser,
     on_delete=models.CASCADE,
     related_name= 'receiver_notifcation',
     blank=True,
     null=True
    )
    job = models.ForeignKey(
        JobManagement,
        related_name = "notification_job",
        on_delete = models.CASCADE
    )
    title = models.CharField(
        "Notification Title",
        max_length=225, blank=True, null=True
    )
    TYPE_OF_NOTIFICATION = (
        ("User_Applied","User_Applied"),
        ("Company_Approved","Company_Approved"),
        ("Company_Review_Rating","Company_Review_Rating"),
        ("JobSeeker_Review_Rating","JobSeeker_Review_Rating")
    )
    type_of_notification = models.CharField(
        "Type of Notification", max_length=200, blank=True, choices=TYPE_OF_NOTIFICATION)
    is_seen = models.BooleanField(
        'Is Seen',
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.sender)

    class Meta:
        verbose_name_plural = "User's Notifications"

#---------------------------Review and Rating------------------------------------------
class ReviewAndRating(models.Model):
    """Review and rating model for both jobseeker and Company"""
    receiver_user = models.ForeignKey(
        MyUser,
        related_name="user_review_rating",
        on_delete=models.CASCADE
    )
    applied_job = models.ForeignKey(
        UserApplyJob,
        related_name="user_applied_job_completion",
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        'Rating',
        default=0
    )
    review = RichTextField("Review",blank=True,null=True)

    def __str__(self):
        return self.receiver_user.email

    class Meta:
        verbose_name_plural = "User Review And Rating"

#----------------------Web Site Contact Us-------------------------
class ContactUsModel(models.Model):
    """Contact Us Model for the site by User"""
    email = models.EmailField(
        "Email",  max_length=50, blank=True,validators=[EMAILREGEX]
    )
    first_name = models.CharField(
        "First Name", max_length=40, validators=[NAMEREGEX], blank=True
    )
    last_name = models.CharField(
        "Last Name", max_length=40, validators=[NAMEREGEX],  blank=True, null=True
    )
    mobile_number=models.CharField("Mobile Number",max_length=16,blank=False, validators=[MOBILEREGEX])
    message=RichTextField("message",blank=False)

    def __str__(self):
        return email

    class Meta:
        verbose_name_plural="Post Contact Us"

#------------------------USER REFERING------------------------------------------------------------
class UserReference(models.Model):
    """Invite people Model"""
    sender = models.ForeignKey(
        MyUser,
        related_name='sender_referer',
        on_delete=models.CASCADE
    )
    receiver = models.EmailField("Reciver",validators=[EMAILREGEX],max_length=50)
    url = models.URLField("Url of site")
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return self.sender.email

    class Meta:
        verbose_name_plural = "Invite User"