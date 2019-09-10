from rest_framework import serializers
from .models import *

#------------------------------About Us Serializer--------------------------
class AboutUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutUs
        fields = ('title','description')

#------------------------------Term and Condition Serializer-------------------
class TermAndConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermsAndConditions
        fields = ('title','description')

#------------------------------Contact Us Serializer-----------------------------
class ContactUsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContactUS
        fields = "__all__"

#----------------Frequent Ask Question Serializer---------------------------------
class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = "__all__"

#------------------Privacy Policy Serializer---------------------------------------
class PolicyPrivacySerializer(serializers.ModelSerializer):
     
     class Meta:
         model = PrivacyPolicy
         fields = "__all__"

#----------------------Who I am Serilaizer-----------------------------------
class WhoIAmSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhoIAm
        fields = "__all__"
