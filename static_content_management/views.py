import cloudinary.uploader 

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

#---------------------------Api Creation for About Us-------------------------
class AboutUsView(APIView):
    """Get api for About Us"""
    def get(self,request):
        instance = AboutUs.objects.latest('id')
        serializer = AboutUsSerializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

#--------------------------Api Creation for Term And Condition-------------------
class TermAndConditionView(APIView):
    """Get Api for Term and Condition"""
    def get(self,request):
        instance  = TermsAndConditions.objects.latest('id')
        serializer  = TermAndConditionSerializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

#---------------------------Api Creation for Contact Us-----------------------------
class ContactUsView(APIView):
    """Get Api for Contact Us"""
    def get(self,request):
        instance = ContactUS.objects.latest('id')
        serializer = ContactUsSerializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

#------------------------Api for FAQ-------------------------------------------------
class FAQView(APIView):
    """Get Api for Frequent Ask Question"""
    def get(self,request):
        instance = FAQ.objects.all()
        serializer = FAQSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

#-------------------Api for Privacy Policy-----------------------------------------
class PolicyPrivacyView(APIView):
    """Get Api for Policy Privacy"""
    def get(self,request):
        instance = PrivacyPolicy.objects.latest('id')
        serializer = PolicyPrivacySerializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

#-------------------------Api for Career-----------------------------------------------
class CareersView(APIView):
    """Post Api for careers"""
    def post(self,request):
        params = request.data
        print("params",params)
        try:
            profession = Profession.objects.get(id=params['profession_id'])
            try:
                instance,create = Career.objects.get_or_create(email=params["email"])
                instance.first_name = params['first_name']
                instance.last_name=params["last_name"]
                instance.profession=profession
                instance.message=params["message"]
                instance.mobile_number=params["mobile_number"]
                instance.save()
                return Response({"message":"Successfully"},status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
        except Exception as e:
            print("Exception", e)
            return Response({"message":"Something Went Wrong!"},status=status.HTTP_400_BAD_REQUEST)

#-------------------------------Resume Uploaded-----------------------------------------------------
class ResumeUploadView(APIView):
    """POST Api for Resume Upload of Career"""
    def post(self,request):
        data = cloudinary.uploader.upload(request.data["resume"])
        instance = Career.objects.get(email=request.data["email"])
        instance.resume = data['url']
        instance.save()
        return Response({"Message":"Resume Upload Successfully","url":data['url']},status=status.HTTP_200_OK)

#--------------------Who I am view-------------------------------------------------
class WhoIAmView(APIView):
    def get(self,request):
        data = WhoIAm.objects.latest('id')
        serializer = WhoIAmSerializer(data)
        return Response(serializer.data)