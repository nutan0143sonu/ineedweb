from django.db import models
from djrichtextfield.models import RichTextField

from cloudinary.models import CloudinaryField
from app.models import Profession

from app.utils import *
#--------------------------------About Us-------------------------------------------------
class AboutUs(models.Model):
    """Model Creation for About us"""
    title = models.CharField("Title", max_length=255, blank=True, null=True)
    description = RichTextField("Description", blank=True, null=True)

    def __str__(self):
        return "About Us"

    class Meta:
        verbose_name_plural = "About Us"

#---------------------------------Term And Condition------------------------------------------
class TermsAndConditions(models.Model):
    """Term And Condition Model"""
    title = models.CharField("Title", max_length=255, blank=True, null=True)
    description = RichTextField("Description", blank=True, null=True)

    def __str__(self):
        return "Terms and conditions"

    class Meta:
        verbose_name_plural = "Terms And Condition"

#----------------------------------Frequest Ask Question---------------------------------
class FAQ(models.Model):
    """Frequency Ask Question Model"""
    question = models.TextField("Question", blank=True, null=True)
    answer = models.TextField("Answer", blank=True, null=True)

    def __str__(self):
        return "FAQ"

    class Meta:
        verbose_name_plural = "FAQ"

#------------------------------Contact Us---------------------------------------------
class ContactUS(models.Model):
    """Contact Us Information Model"""
    title = models.CharField(
        "Title",
        max_length=255, 
        blank=True, 
        null=True
        )
    mobile = models.CharField(
        "Mobile Number",
        max_length=16,
        blank = True,
        null = True,
        validators=[MOBILEREGEX]
    )
    address = models.CharField(
        "Address",
        max_length = 225,
        blank = True,
        null = True
    )
    email = models.EmailField(
        "Email", unique=True, max_length=50, validators=[EMAILREGEX]
    )
    def __str__(self):
        return "Contact Us"

    class Meta:
        verbose_name_plural = "Contact Us"

#-----------------------Privacy Policy------------------------------------
class PrivacyPolicy(models.Model):
    """Privacy and Policy Model of the site"""
    title = models.CharField(
        "Title",
        max_length = 50,
        )
    description = RichTextField("Description", blank=True, null=True)

    def __str__(self):
        return "Privacy Policy"

    class Meta:
        verbose_name_plural = "Privacy Policy"


#---------------------------------------CARRIERS-----------------------------------#
class Career(models.Model):
    """Career Model for site"""
    email = models.EmailField(
        "User Email", 
        unique=False, max_length=50)
    first_name = models.CharField(
        "First Name", max_length=40, 
        blank=True, null=True
    )
    last_name = models.CharField(
        "Last Name", max_length=40, 
        blank=True, null=True
    )
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE, related_name='carrer_profession'
    )
    message = models.TextField(
        "Message", blank=True, null=True
    )
    mobile_number = models.CharField(
        "Mobile Number", max_length=15, blank=True, null=True
    )
    resume = models.URLField(
        "Resume",
        blank = True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Careers"

#------------------------------- Who I am---------------------------------------
class WhoIAm(models.Model):
    """Who I am Model of Site"""
    title = models.CharField(
        "Title",
        max_length = 50,
        )
    description = RichTextField("Description", blank=True, null=True)

    def __str__(self):
        return "Who I am"

    class Meta:
        verbose_name_plural = "Who I am"