import cloudinary.uploader

from django.contrib.auth import authenticate,login,logout

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .sendOtp import *
from .models import *


#----------------------------Forgot Password for App------------------------
class ForgotPaswordView(APIView):
    """
      Forget password for app
       """

    def post(self, request):
        try:
            user = MyUser.objects.get(email=request.data['email'])
            send_OTP(user.otp_verify(), user.email)
            return Response(
                {"message":"Otp send Successfully"},
                status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception",e)
            return Response(
                {"message": "Email not registered."},
                status=status.HTTP_400_BAD_REQUEST)

#--------------------------------Otp Verification for App-------------------------------
class OtpVerficationView(APIView):
    """
          OTP Verification request for App
          params{
              "otp":"123"
          }
          """
    def post(self,request):
        try:
            params = request.data
            user = MyUser.objects.get(email=params['email'])
            if params['otp']==user.otp:
                return Response(
                    {"message":"Successfull Otp verification"},
                    status=status.HTTP_200_OK)
            return Response(
                {"message":"Failed Otp Verification"},
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception as e",e)
            return Response(
                {"message":"Error!"},
                status=status.HTTP_400_BAD_REQUEST)

#--------------------------------Change Password for App----------------------------
class ResetPasswordView(APIView):
    """
    Reset Password request for App
    params{
        "password":"Mobiloitte1",
	    "confirm_password":"Mobiloitte"
    }
    """
    def post(self, request):
        try:
            params = request.data
            user = MyUser.objects.get(email=params['email'])
            print("user",user, params['password'], params['confirm_password'])
            if params['confirm_password']==params['password']:
                user.set_password(params['password'])
                #user.save()
                return Response(
                    {"message":"Succesfull Reset Password"},
                    status=status.HTTP_200_OK)
            return Response(
                {"message":"Password and Confirm Password does not match"},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(
                {"message":"Error!"},
                status=status.HTTP_400_BAD_REQUEST)

#------------------------App Login---------------------------------------------
class LoginView(APIView):
    """
    Login Request
    params{
            "email":"python-trainee1@mobiloitte.com",
	        "password":"Mobiloitte1"
    }
    """
    def post(self,request):
        try:
            params = request.data
            print("params",params)
            user =  authenticate(email=params['email'],password=params['password'])
            print(user)
            if user is not None:
                login(request,user)
                return Response(
                    {"token":user.create_jwt(),
                    "message":"Login successful",
                    "user_type":user.user_type
                    }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "Please enter correct credentials"
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception",e)
#-----------------------Upload image--------------------------------
class ImageUploadView(APIView):
    def post(self,request):
        try:
            image = cloudinary.uploader.upload(request.data['image'])
            print(image['secure_url'])
            return Response(
                {"message": "Image Upload successful",
                 "image_url":image['url']},
                status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Image Upload Failed"},
                status=status.HTTP_400_BAD_REQUEST
            )