#-----------------Packages-----------------------------------#
import json
from datetime import datetime
import cloudinary.uploader
import paypalrestsdk
import logging


#-------------Django packages---------------------------------#
from django.db.models import Sum
from cloudinary.uploader import upload
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate,login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import get_object_or_404
#----------------------Rest framework Packages---------------------#
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
#--------------------Local python file----------------------------#
from .models import *
from app.models import *
from app.sendOtp import *
from .filter import *
from .serializers import *
from .pagination import *
from app.permission import *
from .notification import userNotification
from .payment import *
from .consumers import ChatConsumer


#---------------------Email For SignUp-------------------------------
class RegisterEmailView(APIView):
    """Post Api for Register Email in which we check email is exist or not."""
    def post(self, request):
        try:
            MyUser.objects.get(email=request.data['email'])
            return Response({"message":"Email exist"},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"message":"successful Email registration"},status=status.HTTP_200_OK)

#---------------------SignUpView-------------------------------------
class SignUpView(APIView):
    """Sign Up Post Api for signup as company or job seeker"""
    def post(self,request):
        params = request.data
        try:
            serializers = UserSignupSerializers(data=params, context={"params":params})
            if serializers.is_valid():
                user = serializers.save()
            uid = urlsafe_base64_encode(force_bytes(user.uuid))
            link = params['url']+"/{0}".format(uid.decode('utf8'))
            send_link(link,params['email'])
            return Response({"message":"SignUp successful","uuid":user.uuid},status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception",e)
            MyUser.objects.filter(email=params['email']).delete()
            print("user deleted")
            return Response({"message":"Email already registered on signup"},
                            status=status.HTTP_400_BAD_REQUEST)

#---------------------------------SignUp for Employer ----------------------------------#
class EmployerSignUpView(APIView):
    """Employer Signup Api View"""
    def post(self,request):
        params = request.data
        try:
            serializer = EmployerSignupSerializers(data = params, context = { 'params' : params})
            if serializer.is_valid(raise_exception = True):
                user = serializer.save()
                uid = urlsafe_base64_encode(force_bytes(user.uuid))
                link = params['url']+"/{0}".format(uid.decode('utf8'))
                send_link(link,params['email'])
                return Response({"message":"Signup Successfully Completed","uuid":user.uuid},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Something Went Wrong"},status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception",e)
            MyUser.objects.filter(email=params["email"]).delete()
            print("User Deleted")
            return Response({"message":"Email already registered on signup"},
                            status=status.HTTP_400_BAD_REQUEST)

#----------Image Upload----------------------------------------------------------------------------------
class ImageUploadView(APIView):
    """Image Upload view during signup of Employer and Jobseeker."""
    def post(self,request):
        try:
            image = cloudinary.uploader.upload(request.data['image'])
            return Response(
                {"message": "Image Upload successful",
                 "image_url":image['url']},
                status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Image Upload Failed"},
                status=status.HTTP_400_BAD_REQUEST
            )
class UpdateImage(APIView):
    """Uplaod image View for editing image"""
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            image = cloudinary.uploader.upload(request.data['image'])
            request.user.image = image['url']
            request.user.save()
            return Response(
                    {"message": "Image Upload successful",
                    "image_url":image['url']},
                    status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "Image Upload Failed"},
                status=status.HTTP_400_BAD_REQUEST
            )
#-----------------------------------Email Verify----------------------------------------------------------------
class EmailVerifyView(APIView):
    """Email verification after signup by JobSeeker or Company"""
    def get(self,request,uidb64):
        uid = force_text(urlsafe_base64_decode(uidb64))
        try:
            user = MyUser.objects.get(uuid=uid)
            user.is_active = True
            user.save()
            return Response({"message":"Email Verify"},status=status.HTTP_200_OK)
        except:
            return Response({"message":"Email Verification Failed"},
                            status=status.HTTP_400_BAD_REQUEST)
 #----------------------Industry Model Data-----------------------------
class IndustryView(APIView):
    """Industry View for showing industry data."""
    def get(self,request):
        industry = IndustryModel.objects.all()
        serializer = IndustrySerializer(industry,many=True)
        return Response({
            "data":serializer.data,
            "message":"successful"
        }, status=status.HTTP_200_OK)

#----------------------Area Model Data-----------------------------
class AreaView(APIView):
    """Area View"""
    def get(self,request):
        areaInstance = AreaModel.objects.all()
        serializer = AreaSerializer(areaInstance, many=True)
        return Response({
            "data":serializer.data,
            "message": "successful"
        }, status=status.HTTP_200_OK)

#----------------------Industry Model Data-----------------------------
class ToolsAndLanguageView(APIView):
    """Tool and Language View."""
    def get(self,request):
        toolsAndLanguageInstance = ToolsAndLanguageModel.objects.all()
        serializer = ToolsAndLanguageSerializer(toolsAndLanguageInstance, many=True)
        return Response(
            {
                "data":serializer.data,
                "message":"successful"
            }, status=status.HTTP_200_OK)

#--------------------ForgetPassword for WebSite-------------------------------------
class ForgetPasswordView(APIView):
    """Api or Forget Password and email is also send for verification"""
    def post(self, request):
        try:
            user=MyUser.objects.get(email=request.data['email'])
            uid = urlsafe_base64_encode(force_bytes(user.uuid))
            time = urlsafe_base64_encode(force_bytes(datetime.now()))
            link = request.data['url']+"/{0}/{1}".format(uid.decode('utf8'), time.decode('utf8'))
            send_link(link,request.data['email'])
            return Response({
                "message": "Password reset link is sent to your email address."
                },status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception",e)
            return Response({"message":e},status=status.HTTP_400_BAD_REQUEST)

#--------------------------------Change Password for Website----------------------------
class ResetPasswordView(APIView):
    """Reset Password view"""
    def post(self, request, uidb64, time):
        try:
            user = MyUser.objects.get(uuid=force_text(urlsafe_base64_decode(uidb64)))
            if request.data['confirm_password']==request.data['password']:
                time = parse_datetime(force_text(urlsafe_base64_decode(time)))
                minute = (datetime.now() - time).total_seconds()/60.0
                if minute > 30:
                    return Response({"message":"Successfull"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.set_password(request.data['password'])
                    user.save()
                    return Response(status=status.HTTP_200_OK)
            return Response(
                {
                "message":"Password and Confirm Password does not match"
                },status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response({"message":"Error!"},status=status.HTTP_400_BAD_REQUEST)

#---------------Login User-------------------------------------------------
class LoginView(APIView):
    """Login View"""
    def post(self,request):
        try:
            user =  authenticate(email=request.data['email'],password=request.data['password'])
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
            print(e)
            return Response({"message":"Something went Wrong!"},status=status.HTTP_400_BAD_REQUEST)

#----------------------Change Password -------------------------------------------------------

class ChangePasswordView(APIView):
    """Change Password view"""
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            if request.user.check_password(request.data['old_password']):
                request.user.set_password(request.data['new_password'])
                request.user.save()
                return Response(
                    {"message":"Password Updated successfuly"},
                    status=status.HTTP_200_OK)
            return Response(
                {"message":"Old Password does not match with exist Password"},
                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {"message":"Error!"},
                status=status.HTTP_400_BAD_REQUEST)

#----------------profile  View-------------------------------------------------
class ProfileView(APIView):
    """Jobseeker Profile View"""
    permission_classes = (JobSeekerAuthentication,)
    def get(self,request):
        user = request.user
        num = user.user_skill.count()
        total=num*5
        rating = user.user_skill.aggregate(Sum('rating'))['rating__sum']
        experience_level = ''
        try:
            per=int(rating/total)*100
            if per >=75:
                experience_level ="Proficial"
            elif per<=40:
                experience_level ="Beginner"
            else:
                experience_level="intermediate"    
        except Exception as  Unsupported:
            experience_level ="Beginner" 
        serializer = UserSerializer(user)
        return Response(
            {
            "message":"successful","data":serializer.data,
            "experience_level":experience_level
            },status=status.HTTP_200_OK)

#-----------------Job Seeker Edit Profile-----------------------------------------------------------
class JobSeekerEditProfileStep1(APIView):
    """Job Seeker Editing Profile Step 1"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        request.user.first_name=request.data['first_name']
        request.user.last_name=request.data['last_name']
        if request.data['password']==request.data['confirm_password']:
            request.user.set_password(request.data['password'])
            request.user.save()
            return Response({"message":"Successful Updation"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"password Does not match to confirm password"},status=status.HTTP_400_BAD_REQUEST)
class JobSeekerEditProfileStep2(APIView):
    """Job Seeker Editing Profile Step 2"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
            try:
                params=request.data
                area = request.user.user_area.filter(user=request.user).delete()
                industry = request.user.user_industry.filter(user=request.user).delete()
                skill = request.user.user_skill.filter(user=request.user).delete()
                for data in params['area']:
                    area,create = AreaModel.objects.get_or_create(area=data)
                    UserAreaModel.objects.create(user=request.user,area=area)
                for industry in params['industry']:
                    indus,create = IndustryModel.objects.get_or_create(industry_type=industry)
                    UserIndustryModel.objects.create(user=request.user,industry=indus)
                for tools_language in params['tool_and_languages']:
                    lang,create = ToolsAndLanguageModel.objects.get_or_create(name=tools_language)
                    UserToolsAndLanguageModel.objects.create(user=request.user,skill=lang,)
                serializer = UserEditProfileSerializer(request.user)
                return Response({"data":serializer.data,"message":"Successful"},status=status.HTTP_200_OK)
            except Exception as e:
                print("Exception",e)
                return Response({"message":"Something Went Wrong"},status = status.HTTP_400_BAD_REQUEST)


class JobSeekerEditProfileStep3(APIView):
    """Job Seeker Editing Profile Step 3"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        params=request.data
        for key,data in params['tool_and_language'].items():
            obj= request.user.user_skill.get(skill__name=key)
            obj.rating = data
            obj.save()
        ins = request.user.user_personal_detail
        ins.professional_title=params['professional_title']
        ins.professional_description=params['professional_description']
        ins.paypal_account_id=params['paypal_account_id']
        ins.save()
        return Response({"message":"Successfully Updated"},status=status.HTTP_200_OK)       


#--------------------------Working Hour In A week view------------------------------------#
class WorkingHourView(APIView):
    """Get api for Working Hour of posted job"""
    def get(self,request):
        working = WorkingHourModel.objects.all()
        serializer = WorkingHourSerializer(working,many=True)
        return Response(
            {"message":"successfull",
             "data":serializer.data
             }, status=status.HTTP_200_OK)

#--------------------------Availability and location View---------------------------------
class AvailabilityAndLocationView(APIView):
    """Job Seeker Availability and Locality Api"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        params = request.data
        data = PersonalDetailModel.objects.get(user__id=request.user.id)
        data.mobile=params['mobile']
        data.city=params['city']
        data.postal_code=params['postal_code']
        data.country=params['country']
        data.timezone=params['timezone']
        data.work_hour=WorkingHourModel.objects.get(id=params['work_hour'])
        data.save()
        return Response({"message":"Successfully Updated"},status=status.HTTP_200_OK)

class GetAvailabilityAndLocationView(APIView):
    """Api Creation for getting job seeker Availability and locality."""
    permission_classes = (JobSeekerAuthentication,)
    def get(self,request):
            instance = PersonalDetailModel.objects.filter(user=request.user)
            serializer = AvailabilityAndLocationSerializer(instance ,many=True)
            return Response({"message":"Successfully","data":serializer.data},status=status.HTTP_200_OK)
            
#---------------------------Language View-------------------------------------------------
class SpeakingLanguageView(APIView):
    """Api Creation for getting speaking language for post job and jobseeker known."""
    def get(self,request):
        instance = SpeakingLanguageModel.objects.all()
        serializer = SpeakingLanguageSerializer(instance,many=True)
        return Response(
            {"message":"Successfull",
             "data":serializer.data
             },
            status=status.HTTP_200_OK
        )

#-------------------------------Employment History View----------------------------------------------------
class EmploymentHistoryView(APIView):
    """Api creation for Employment history of job seeker."""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        try:
            params = request.data
            print("params",request.data,params)
            params['user']=request.user.id
            serializer = EmploymentHistorySerializer(data=params,context={"params":params})
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message":"successfull",
                     "data":serializer.data
                     },status=status.HTTP_200_OK)
            return Response(
                {"message":"Failed!",
                 "erorr":serializer.errors
                 },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("exception",e)
            return Response(
                {"message":"something went Wrong!"},
                status=status.HTTP_400_BAD_REQUEST)

class EmploymentHistoryDeleteView(APIView):
    """Api creation for deletion of employement history of jobseeker."""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        try:
            UserEmploymentHistoryModel.objects.get(id=request.data['employment_history_id']).delete()
            return Response({"message":"Successful deleted"},status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception",e)
        return Response({"message":"Something Went Wrong"},status = status.HTTP_400_BAD_REQUEST)


class GetEmploymentHistoryView(APIView):
    """Api for getting job seeker employeement history"""
    permission_classes = (JobSeekerAuthentication,)
    def get(self,request):
        emp = UserEmploymentHistoryModel.objects.filter(user=request.user)
        serializer = EmploymentHistorySerializer(emp,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)

#----------------User Education View---------------------------------------------------------------
class UserEducationView(APIView):
    """Api for posting jobseeker Education"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        try:
            params = request.data
            params['user'] = request.user.id
            serializer = UserEducationSerializer(data=params,context={"params":params})
            if serializer.is_valid():
                uev = serializer.save()
                return Response(
                    {"message":"successfully",
                    "data":serializer.data
                    },status=status.HTTP_200_OK )
            return Response(
                {"message": "Failed!",
                "erorr": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception",e)
            return Response(
                {"message":"something went Wrong!"},
                status=status.HTTP_400_BAD_REQUEST)


class GetUserEducationView(APIView):
    """Api for getting jobseeker education"""
    permission_classes = (JobSeekerAuthentication,)
    def get(self,request):
        userEducationInstance = UserEducationModel.objects.filter(user=request.user)
        serializer = GetUserEducationSerializer(userEducationInstance,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
        
class UserEducationDeleteView(APIView):
    """Api for deleting job seeker education"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        try:
            UserEducationModel.objects.get(id=request.data['user_education_id']).delete()
            return Response({"message":"Successful deleted"},status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception",e)
        return Response({"message":"Something Went Wrong"},status = status.HTTP_400_BAD_REQUEST)

#-----------------user Language View---------------------------------------------------------------
class UserLanguageView(APIView):
    """Api for posting job seeker known language."""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        try:  
            userLanguage = request.user.user_language.filter().delete()
            for data,key in request.data['user_language'].items():
                lang,create = SpeakingLanguageModel.objects.get_or_create(language_name=data)
                obj= UserLanguageModel.objects.create(user=request.user,userLanguage=lang,rating=key)
            return Response({"message":"Successful Updation"},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "something went Wrong!"}, status=status.HTTP_400_BAD_REQUEST)

class GetUserLanguageView(APIView):
    """Api for getting job seeker language."""
    permission_classes = (JobSeekerAuthentication,) 
    def get(self,request):
        my_list=[]
        lang = request.user.user_language.filter()
        for data in lang:
            fluency = ""
            if data.rating==1 or 0:
                fluency="Elemetry"
            elif data.rating==2:
                fluency="Intermediate"
            elif data.rating==3:
                fluency="Working proficiency"
            elif data.rating==4:
                fluency="Advanced"
            else:
                fluency="Mother tongue / Fluent"
            mydict = {
                "id":data.id,
                "name":data.userLanguage.language_name,
                "rating":data.rating,
                "Level":fluency
            }
            my_list.append(mydict)
        return Response(my_list,status=status.HTTP_200_OK)
                    
#----------------------------POST JOB Post Api-----------------------------------------------------#
class PostJobView(APIView):
    """Api for posting job step1 by company"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        try:
            job = JobManagement.objects.create(
                user=request.user,
                jobTitle=request.data['jobTitle'],
                jobDiscription=request.data['jobDiscription']
                )
            for data in request.data['area']:
                workArea,create = AreaModel.objects.get_or_create(area=data)
                PostJobAreaModel.objects.create(job=job,area=workArea)
            serializer = PostJobStep2serailizer(job)    
            return Response({"data":serializer.data,"message":"Successful"},status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception",e)
            return Response({"message":"Something Went Wrong"},status = status.HTTP_400_BAD_REQUEST)

class PostJobStep2(APIView):
    """Api for posting job step2 by company"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        try:
            post_job = JobManagement.objects.get(id=request.data['id'])
            post_job.requiredAnalytics = request.data['requiredAnalytics']
            post_job.save()
            PostJobSkillModel.objects.filter(job=post_job).delete()
            for data in request.data['skills']:
                skill,create = ToolsAndLanguageModel.objects.get_or_create(name=data)
                PostJobSkillModel.objects.create(job=post_job,skills=skill)
            serializer = PostJobStep2serailizer(post_job)
            return Response({"data":serializer.data,"message":"Successful"},status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception",e)
            return Response({"message":"Something Went Wrong"},status = status.HTTP_400_BAD_REQUEST)

class PostJobStep3(APIView):
    """Api for posting job step3 by company"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        try:
            params=request.data
            post_job = JobManagement.objects.get(id=params['id'])
            post_job.type_of_project=params['project_type']
            post_job.save()
            PostJobPreferenceLanguageModel.objects.filter(job=post_job).delete()
            PostJobPreferenceLocationModel.objects.filter(job=post_job).delete()
            for data in params['preference_language']:
                lang,create = SpeakingLanguageModel.objects.get_or_create(language_name=data)
                PostJobPreferenceLanguageModel.objects.create(job=post_job,preferenceLanguage=lang)
            for location in params['preference_location']:
                loc,create = Location.objects.get_or_create(locationName=location)
                PostJobPreferenceLocationModel.objects.create(job=post_job,preferenceLocation=loc)
            serializer = PostJobStep2serailizer(post_job)
            return Response({"data":serializer.data,"message":"Successful"},status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception of Step3",e)
            return Response({"message":"Something Went Wrong"},status = status.HTTP_400_BAD_REQUEST)

class PostJobStep4(APIView):
    """Api for posting job step4 by company"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        params = request.data
        try:
            post_job = JobManagement.objects.get(id=params['id'])
            post_job.payment=params['payment']
            post_job.duration=params['duration']
            salary,create = Salary.objects.get_or_create(salaryPerHour=params['salary'])
            post_job.desiredSalary=salary
            post_job.is_active = True
            post_job.save()
            serializer = PostJobStep2serailizer(post_job)
            return Response({"data":serializer.data,"message":"Successful"},status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception of step 4",e)
            return Response({"message":"Something Went Wrong"},status = status.HTTP_400_BAD_REQUEST)

#-----------------------Posted Job Get Api-----------------------------------------------------------
class GetPostedJobView(APIView):
    """Api for getting posted job by company."""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        data = matchingJobfilter(request,'nothing',context="getPostedJob")
        page = request.data['page']
        limit = 5
        list2, page, paginator = paginatorData(data, limit, page)
        serializer = EmployerPostedJobSerializer(list2, many=True)
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(data), "pages": paginator.num_pages,
                                          "limit": limit}}, status=status.HTTP_200_OK)

#------------------Single Posted Job api-------------------------------------------------------------
class SinglePostedJobView(APIView):
    """Api for getting single posted job by company."""
    permission_classes = (EmployerAuthentication,)
    def get(self,request):
        instance = JobManagement.objects.get(id=request.data['id'])
        serializer = EmployerPostedJobSerializer(instance)
        return Response(
            serializer.data
        )

#-----------------Single Posted Job Deletion api----------------------------------------------------
class SinglePostedJobDeletion(APIView):
    """Api for deleting single posted job"""
    permission_classes = (EmployerAuthentication,)
    def get(self,request):
        instance = JobManagement.objects.get(id=request.data['id']).delete()
        return Response({"message":"Successfully Deleted"},status=status.HTTP_200_OK)

#--------------------------Post Job Editing Api for Step1-------------------------------------------
class EditPostedJobStep1(APIView):
    """Api for editing posted job step1."""
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        instance = JobManagement.objects.get(id=request.data['id'])
        serializer = EditPostedJobStep1Serializer(instance,data=request.data,context={"params":request.data})
        if serializer.is_valid(raise_exception = True):
            comment = serializer.save()
            return Response({"data":serializer.data,"message":"Successfull Edition of Step 1"},status=status.HTTP_200_OK)
        return Response({"message":"SomeThing Went Wrong"},status=status.HTTP_400_BAD_REQUEST)

#-------------------------GET NOTIFICATION--------------------------------------------------------------#

class NotificationAllGet(APIView):
    """Api for getting all notification of user."""
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        instance=Notification.objects.filter(receiver=request.user)
        serializer=NotificationSerializer(instance,many=True)
        return Response({"data":serializer.data,"message":"Successfull"},status=status.HTTP_200_OK)

class NotificationSeen(APIView):
    """Notification api for seen by user"""
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        instance = Notification.objects.get(id=request.data['notification_id'])
        instance.is_seen=True
        instance.save()
        return Response({"message":"Successfull"},status=status.HTTP_200_OK)

class GetSingleNotification(APIView):
    """Get api for getting notification"""
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        notification=Notification.objects.get(id=request.data['notification_id'])
        if notification.type_of_notification=="User_Applied":
            user = UserSerializer(notification.sender)
            my_serializer = UserApplyJobSerializer(UserApplyJob.objects.get(user=notification.sender,job=notification.job))
            user_detail = user.data
            user_detail['User_Resume']=my_serializer.data
            return Response({"data":user_detail},status=status.HTTP_200_OK)
        elif notification.type_of_notification=="Company_Approved":
            job = JobSeekerjobSerailizer(notification.job)
            return Response({"data":job.data},status=status.HTTP_200_OK)
        elif notification.type_of_notification=="Company_Review_Rating":
            user_applied_job = UserApplyJob.objects.get(user=notification.receiver,job=notification.job)
            review = ReviewAndRatingSerializer(ReviewAndRating.objects.get(user=user_applied_job.user,applied_job=user_applied_job))
            return Response({"data":review.data},status=status.HTTP_200_OK)
        else:
            user_applied_job = UserApplyJob.objects.get(user=notification.sender,job=notification.job)
            review = ReviewAndRatingSerializer(ReviewAndRating.objects.get(user=user_applied_job.job.user,applied_job=user_applied_job))
            return Response({"data":review.data},status=status.HTTP_200_OK)

#---------------------------Salary-----------------------------------------------------------------#
class SalaryPerHourView(APIView):
    """Get Api for Salary"""
    def get(self,request):
        instance = Salary.objects.all()
        serializer = SalarySerializer(instance,many=True)
        return Response({"data":serializer.data,"message":"successfully"},status=status.HTTP_200_OK)
#----------------------------------------Employer Profile-------------------------
class EmployerProfile(APIView):
    """Get Api for company profile"""
    permission_classes = (EmployerAuthentication,)
    def get(self,request):
        job_count = request.user.company.count()
        serializer = EmployerProfileSerializer(request.user)
        if serializer:
            return Response({"data":serializer.data,"Total Posted Job":job_count,"message":"successful"},status=status.HTTP_200_OK)
        return Response({"message":"Something Went Wrong!"},status=status.HTTP_400_BAD_REQUEST)

#------------------------- Location---------------------------------------------------------------# 
class LocationView(APIView):
    """Get Api for location"""
    def get(self,request):
        instance = Location.objects.all()
        serializer = LocationSerializer(instance,many=True)
        return Response({"data":serializer.data,"message":"successfully"},status=status.HTTP_200_OK)

#-----------------------------------User Matching Job Api-----------------------------------------------
class MatchingJob(APIView):
    """Matching Job Api for Jobseeker"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        try:
            user_skills = request.user.user_skill.all().values_list('skill',flat=True)
            skill = PostJobSkillModel.objects.filter(skills__in=user_skills).distinct('job')
            job_id = skill.values_list('job__id',flat=True)
            data = matchingJobfilter(request,job_id,context="userMatchigngJob")
            applied_job = request.user.user_favourite.filter(job__id__in=job_id).values_list('job_id',flat=True)
            limit = 10
            list2, page, paginator = paginatorData(data, limit, request.data['page'])
            serializer = JobSeekerjobSerailizer(list2,many=True, context={"applied_job":applied_job,"user":request.user})
            return Response({"data": serializer.data, "message": "Fetched data successfully",
                        "pagination_data": {"page": page, "total": len(data), "pages": paginator.num_pages,
                                            "limit": limit}}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

#---------------------User Favourite job Api---------------------------------------------------------             
class UserFavouriteJobView(APIView):
    """Favourite job Api for Jobseeker"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        fav,obj = UserApplyJob.objects.get_or_create(user=request.user,
            job=JobManagement.objects.get(id=request.data['job_id']))
        fav.is_favourite=request.data["favourite"]
        fav.save()
        return Response({"message":"Successfully Updated"},status=status.HTTP_200_OK)

class GetUserFavouriteJobView(APIView):
    """Get jobseeker favourite job"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        job_id = request.user.user_favourite.filter(is_favourite=True).values_list("job__id",flat=True)
        data = matchingJobfilter(request,job_id,context='favoriteJob')
        page = request.data['page']
        limit = 5
        list2, page, paginator = paginatorData(data, limit, page)
        serializer = JobSeekerjobSerailizer(list2,many=True, context={"applied_job":job_id,"user":request.user})

        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(data), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK)


#---------------------------User Apply Job Api------------------------------------
class UserApplyJobView(APIView):
    """Api of apply job by jobseeker"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        params = request.data
        job_management = JobManagement.objects.get(id=params['job_id'])
        job,obj = UserApplyJob.objects.get_or_create(
         user=request.user,
         job=job_management
        )
        job.hire_question=params['hire_question']
        job.is_apply=True
        job.save()
        title = request.user.first_name + " " +\
                request.user.last_name + " has applied for "+\
                job_management.jobTitle +" job whic has been posted on "+ str(job_management.created_at)
        type_of_notification = "User_Applied"
        userNotification(request.user,job_management.user,job_management,title,type_of_notification)
        return Response({"message":"Successfully Applied","Notfication":"Successfullu notification send"},status=status.HTTP_200_OK)

#-------------------------------Resume Uploaded-----------------------------------------------------
class UserResumeUploadView(APIView):
    """POST Api for Resume Upload of Career"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        data = cloudinary.uploader.upload(request.data["resume"])
        instance = UserApplyJob.objects.get(user=request.user,
        job=JobManagement.objects.get(id=request.data['job_id']))
        instance.resume = data['url']
        instance.save()
        return Response({"Message":"Resume Upload Successfully","url":data['url']},status=status.HTTP_200_OK)

#------------------------------User Applied Job GET Api-------------------------------------------------
class UserAppliedJob(APIView):
    """Api for job seeker apply job"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        job_id = request.user.user_favourite.filter(is_apply=True).values_list("job__id",flat=True)
        applied_job = request.user.user_favourite.filter(job__id__in=job_id).values_list('job_id',flat=True)
        data = matchingJobfilter(request,job_id,context='userApplyJob')
        page = request.data['page']
        limit = 5
        list2, page, paginator = paginatorData(data, limit, page)
        serializer = JobSeekerjobSerailizer(list2,many=True, context={"applied_job":applied_job,"user":request.user})
        return Response({"data": serializer.data, "message": "Fetched Data successfully",
                     "pagination_data": {"page": page, "total": len(data), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK)
       
        return Response(serializer.data,status=status.HTTP_200_OK)

#------------------Company Edit View-----------------------------------------------------------------------
class UserCompanyEditView(APIView):
    """Edit Company Profile"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        request.user.first_name = request.data['company_name']
        request.user.save()
        return Response({"message":"successfully done"},status=status.HTTP_200_OK)

class UserIndustryEditView(APIView):
    """Edit company Industry data"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        industry = request.user.user_industry.filter().delete()
        try:
            for data in request.data['industry_type']:
                indus,create = IndustryModel.objects.get_or_create(industry_type=data)
                UserIndustryModel.objects.create(user=request.user,industry=indus)
            return Response({"message":"Successfully Update"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"Something Went Wrong!","Excption":e},status=status.HTTP_200_OK)

#-------------------------Employer Active Job Api ----------------------------------------------------------
class EmployerActiveJob(APIView):
    """Company Active Job api"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        job = UserApplyJob.objects.filter(job__user=request.user,is_apply=True,employer_is_completed=False)
        data = employerActiveJobFilter(request,job)
        limit = 5
        list2, page, paginator = paginatorData(data, limit, request.data['page'])
        serializer = EmployerActiveJobSerializer(list2,many=True)
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                        "pagination_data": {"page": page, "total": len(data), "pages": paginator.num_pages,
                                            "limit": limit}}, status=status.HTTP_200_OK)   
        
#-------------------------Employer Job Api------------------------------------------------------------
class EmployerJobApplicant(APIView):
    """Company All applicant who applied of a particular company jobs"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        try:
            job = UserApplyJob.objects.filter(job__user=request.user).values_list("user__email",flat=True).distinct('user__email')
            result = applicantFilter(request,job)
            limit = 5
            list2, page, paginator = paginatorData(result, limit,  page = request.data['page'])
            serializer = UserSerializer(list2,many=True)
            return Response({"data": serializer.data, "message": "Fetched data successfully",
                        "pagination_data": {"page": page, "total": len(result), "pages": paginator.num_pages,
                                            "limit": limit}}, status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({"message":"Somehing Went Wrong!","Exception":e},status=status.HTTP_400_BAD_REQUEST)  
       
class AllApplicantOfPostedJob(APIView): 
    """All aplicant of a particular posted job by company""" 
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        job = UserApplyJob.objects.filter(job__id=request.data['job_id']).values_list("user__email",flat=True)
        result = applicantFilter(request,job)
        limit = 5
        list2, page, paginator = paginatorData(result, limit,  page = request.data['page'])
        serializer = UserSerializer(list2,many=True)
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(result), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK) 
#----------------------------Message Chat Api----------------------------------------------------------------------
class ApplicationAcceptance(APIView):
    """This Api Called when company accept applicant message request after applied job"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        applied_job = UserApplyJob.objects.get(id=request.data['user_applied_job_id'])
        applied_job.is_accepted = True
        applied_job.save()
        message = ChatModel.objects.create(
            sender=applied_job.user,
            receiver=request.user,
            accepted_applied_job=applied_job,
            message = "Let's Chat"
        )
        return Response({"message":"Successfully accepted applicants request"},status=status.HTTP_200_OK)
class GetMessageView(APIView):
    """Get all Chat of particular job"""
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        chat = ChatModel.objects.filter(
            accepted_applied_job=UserApplyJob.objects.get(id=request.data['user_applied_job_id'])
            )
        is_seen=chat.filter(receiver=request.user,is_seen=False).update(is_seen=True)
        serializer = ChatSerializer(chat,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
# class MessageView(APIView):
#     """Now Chat Between Employer and job_seeker of particular job"""
#     permission_classes = (IsAuthenticated,)
#     def post(self,request):
#         job = UserApplyJob.objects.get(id=request.data['user_applied_job_id'])
#         data = ChatConsumer()
#         print("data",data)
#         # if request.user.user_type!="Job Seeker":
#         #     ChatModel.objects.create(
#         #         sender = request.user,
#         #         receiver = job.user,
#         #         message = request.data["message"],
#         #         accepted_applied_job=job
#         #     )
#         # else:
#         #     ChatModel.objects.create(
#         #         sender = request.user,
#         #         receiver = job.job.user,
#         #         message = request.data["message"],
#         #         accepted_applied_job=job
#         #     )
#         return Response({"message":"Message Successfully Sended"},status=status.HTTP_200_OK)

class MessageAttachment(APIView):
    """If user use attachment during chat then this api will call and form-data is used here as a request"""
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        job = UserApplyJob.objects.get(id=request.data['user_applied_job_id'])
        data = cloudinary.uploader.upload(request.data["attachment"])
        if request.user.user_type!="Job Seeker":
            ChatModel.objects.create(
                sender = request.user,
                receiver = job.user,
                message = data['url'],
                is_attachment=True,
                accepted_applied_job=job
            )
        else:
            ChatModel.objects.create(
                sender = request.user,
                receiver = job.job.user,
                message = data['url'],
                is_attachment=True,
                accepted_applied_job=job
            )
        return Response({"message":"Message Successfully Sended"},status=status.HTTP_200_OK)

class GetallMessage(APIView):
    """Get all Applicant message of a particular employer"""
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        my_list = []
        if request.user.user_type=="Company":
            accepted_applicant = UserApplyJob.objects.filter(job__user=request.user,is_accepted=True,is_apply=True)
            for data in accepted_applicant:
                message  = ChatModel.objects.filter(accepted_applied_job=data).order_by('-id')[:1]
                instance = message[0]
                my_dict={
                    "Applicant":data.user.email,
                    "Employer":data.job.user.email,
                    "applicant_accepted_id":data.id,
                    "created_at":instance.created_at,
                    "is_attachment":instance.is_attachment,
                    "last_message":instance.message,
                    "image":data.user.image,
                    "first_name":data.user.first_name,
                    "last_name":data.user.last_name
                }
                my_list.append(my_dict)
        else:
            accepted_applicant = UserApplyJob.objects.filter(user=request.user,is_accepted=True,is_apply=True)
            for data in accepted_applicant:
                message  = ChatModel.objects.filter(accepted_applied_job=data).order_by('-id')[:1]
                instance = message[0]
                my_dict={
                    "Applicant":data.user.email,
                    "Employer":data.job.user.email,
                    "applicant_accepted_id":data.id,
                    "created_at":instance.created_at,
                    "is_attachment":instance.is_attachment,
                    "last_message":instance.message,
                    "image":data.job.user.image,
                    "first_name":data.job.user.first_name,
                    "last_name":data.job.user.last_name
                }
                my_list.append(my_dict)
        return Response(my_list,status=status.HTTP_200_OK)

#------------------------------------Job Seeker Active job API--------------------------------------
class EmployerApprovedJob(APIView):
    """Api for approving job by employer"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        user_apply_job = UserApplyJob.objects.get(id=request.data['user_applied_job_id'])
        user_apply_job.is_approved = True
        user_apply_job.save()
        job = JobManagement.objects.get(id=user_apply_job.job.id)
        job.approved_employee = job.approved_employee+1
        job.save()
        if job.requiredAnalytics == job.approved_employee:
            job.is_active = False
            job.save()
        title = job.user.first_name +" has been approved your " +job.jobTitle +" job"
        userNotification(request.user,user_apply_job.user,job,title,type_of_notification="Company_Approved")
        return Response({"message":"Succesfully Approved","notification":"Notification is send successfully"},status=status.HTTP_200_OK)

#---------------------------Job Seeker Active Job Api View--------------------------------------------
class GetUserActiveJob(APIView):
    """Api for JobSeeker Active job after Approving Job """
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        job = request.user.user_favourite.filter(
            is_approved=True,
            is_apply=True,
            job_seeker_is_completed=False,
            employer_is_completed=False
            ).values_list("job__id",flat=True)
        data = matchingJobfilter(request,job,context='activeJob')
        limit = 5
        list2, page, paginator = paginatorData(data, limit, request.data['page'])
        serializer = JobSeekerjobSerailizer(list2,many=True, context={"applied_job":job,'user':request.user})
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(data), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK)    

#------------------------------------Job Seeker Completed Job-------------------------------------------------
class JobSeekerCompletedJob(APIView):
    """Job seeker completed job api."""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        job = request.user.user_favourite.get(id=request.data['user_applied_job_id'])
        job.job_seeker_is_completed = True
        job.save()
        review_rating,obj = ReviewAndRating.objects.get_or_create(
             receiver_user=job.job.user,applied_job=job
            )
        review_rating.rating=request.data['rating']
        review_rating.review=request.data['review']
        review_rating.save()
        title = request.user.first_name + request.user.last_name + \
            " has mention successfully completion of "+job.job.jobTitle +" job and also given review and rating."
        userNotification(request.user,job.job.user,job.job,title,type_of_notification="JobSeeker_Review_Rating")
        return Response(
            {
                "message":"Successfully Job Seeker job Completed",
                "review_and_rating":"Successfully given review and rating",
                "Notification":"Successfully send Notification"
            },status=status.HTTP_200_OK)

#------------------------------------Job Seeker Pending Job-------------------------------------------------
class JobSeekerPendingJob(APIView):
    """Job Seeker Pendng job api"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        job = request.user.user_favourite.filter(
            user=request.user,
            is_apply=True,
            is_accepted=True,
            is_approved=True,
            job_seeker_is_completed=True,
            employer_is_completed=False
            ).values_list("job__id",flat=True)
        data = matchingJobfilter(request,job,context='pendingJob')
        limit = 5
        list2, page, paginator = paginatorData(data, limit, request.data['page'])
        serializer = JobSeekerjobSerailizer(data,many=True, context={"applied_job":job,'user':request.user})
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(data), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK) 

class JobSeekerCompletedJobView(APIView):
    """Job seeker completed job api"""
    permission_classes = (JobSeekerAuthentication,)
    def post(self,request):
        job = request.user.user_favourite.filter(
            user=request.user,
            is_approved=True,
            is_apply=True,
            job_seeker_is_completed=True,
            employer_is_completed=True
            )
        applied_job = job.values_list("job__id",flat=True)
        data = matchingJobfilter(request,applied_job,context='completedJob')
        limit = 5
        list2, page, paginator = paginatorData(data, limit, request.data['page'])
        serializer = JobSeekerComletedJobSerializer(data,many=True, context={"applied_job":applied_job,'user':request.user})
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                        "pagination_data": {"page": page, "total": len(data), "pages": paginator.num_pages,
                                            "limit": limit}}, status=status.HTTP_200_OK)      

#-------------------------Company will sure complete job of jobseeker-------------------------------------
class EmployerCompleteJobForJobSeeker(APIView):
    """Company completed job post api of jobseeker"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        job = UserApplyJob.objects.get(id=request.data['user_applied_job_id'])
        job.employer_is_completed = True
        job.save()
        review_rating,obj = ReviewAndRating.objects.get_or_create(
            receiver_user=job.user,applied_job=job
            )
        review_rating.rating=request.data['rating']
        review_rating.review=request.data['review']
        review_rating.save()
        title = request.user.first_name + " has approve completion of " + job.job.jobTitle + " and also given review and rating."
        userNotification(request.user,job.user,job.job,title,type_of_notification="Company_Review_Rating")
        return Response(
            {
                "message":"Successfully Employer confirm completeion of job Job seeker",
                "review_and_rating":"Successfully given review and rating",
                 "Notification":"Successfully send Notification"
            },status=status.HTTP_200_OK)

class EmployerCompleteJob(APIView):
    """Company Completed all jobs get api"""
    permission_classes = (EmployerAuthentication,)
    def post(self,request):
        user_completed_job =UserApplyJob.objects.filter(job__user=request.user,employer_is_completed=True)
        data = employerActiveJobFilter(request,user_completed_job)
        page = request.data['page']
        limit = 5
        list2, page, paginator = paginatorData(data, limit, page)
        serializer = EmployerCompletedJobSerializer(data,many=True)
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(data), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK)   
       
       
    

#----------------------Top Skills section------------------------------------------------------------
class TopSkillJobSeekerView(APIView):
    """Job seeker top skill api"""
    def post(self,request):
        jobseeker = UserToolsAndLanguageModel.objects.filter(skill__name=request.data['skill']).values_list("user__email",flat=True)
        user = MyUser.objects.filter(email__in=jobseeker)
        limit = 10
        list2, page, paginator = paginatorData(user, limit, request.data['page'])
        serializer = UserSerializer(list2,many=True)
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(user), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK) 

class TopSkillCompanyView(APIView):
    """Company top skill api"""
    def post(self,request):
        company = PostJobSkillModel.objects.filter(skills__name=request.data['skill']).values_list("job__id",flat=True)
        job = JobManagement.objects.filter(id__in=company,is_active=True)
        limit = 10
        list2, page, paginator = paginatorData(job, limit, request.data['page'])
        serializer = EmployerPostedJobSerializer(list2,many=True)
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(job), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK) 
        

#------Post contact Us------------------------- 
class PostContactUsView(APIView):
    """APi for contact us."""
    def post(seld,request):
        params=request.data
        serializer=PostContactUsSerailizer(data=params)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
        return Response({"message": "Successfully","data":serializer.data})

#-------------------Looking for Jobseeker-------------------------------------------
class JobSeekerView(APIView):
    """All jobseeker get api"""
    def post(self,request):
        user = MyUser.objects.filter(user_type="Job Seeker")
        page = request.data['page']
        limit = 10
        list2, page, paginator = paginatorData(user, limit, request.data['page'])
        serializer = UserSerializer(user,many=True)
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(user), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK) 

#---------------------------------Looking for cmpany------------------------------------
class CompanyView(APIView):
    """All company get api"""
    def post(self,request):
        job = LookingForJob(request)
        limit = 10
        list2, page, paginator = paginatorData(job, limit, request.data['page'])
        serializer = EmployerPostedJobSerializer(job,many=True)
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(job), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK) 

#---------------------------------top 10 company-----------------------------------------
class Top10Company(APIView):
    """Top 10 company api"""
    def post(self,request):
        company = MyUser.objects.filter(user_type="Company")
        limit = 5
        list2, page, paginator = paginatorData(company, limit, request.data['page'])
        serializer = Top10CompanySerializer(list2,many=True)
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(company), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK) 
#----------------------------Top 10 Job Seeker--------------------------------------------
class Top10JobSeeker(APIView):
    """Top 10 jobseeker api"""
    def post(self,request):
        jobseeker = MyUser.objects.filter(user_type="Job Seeker")
        limit = 5
        list2, page, paginator = paginatorData(jobseeker, limit, request.data['page'])
        serializer = Top10JobSeekerSerializer(list2,many=True)
        return Response({"data": serializer.data, "message": "Fetched data successfully",
                     "pagination_data": {"page": page, "total": len(jobseeker), "pages": paginator.num_pages,
                                         "limit": limit}}, status=status.HTTP_200_OK) 
#----------------------------Post User Reference------------------------------------------
class Invite(APIView):
    """Refer Site to any user api"""
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        email = send_template_reference(
            request.data['url'],
            request.user.email,
            request.data['receiver'],
            request.user.first_name)
        UserReference.objects.create(
            sender=request.user,
            receiver=request.data['receiver'],
            url=request.data['url'])
        return Response({"message":"Successfuly sended invitation"})

#-----------------Testing for languages changes---------------------------------------------
class JobSeekerTestingView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        # user = MyUser.objects.filter(user_type="Job Seeker")
        # page = request.data['page']
        # limit = 10
        # list2, page, paginator = paginatorData(request.user, limit, page)
        user = request.user
        next_data = MyUser.objects.filter(id__gt=user.id).order_by('id').first()
        print("next_data",next_data)
        serializer = UserTestingSerializer(user)
        # return Response({"data": serializer.data, "message": "Fetched data successfully",
        #              "pagination_data": {"page": page, "total": len(user), "pages": paginator.num_pages,
        #                                  "limit": limit}}, status=status.HTTP_200_OK) 
        return Response(serializer.data)

#--------------------------------Paypal----------------------------------
class PayPal(APIView):
    def get(self,request):
        payment = paypal_payment()
        payment = {"payment":payment}
        return Response({"message":"seuccessful"})

class Excute(APIView):
    def get(self,request):
        logging.basicConfig(level=logging.INFO)

        payment = paypalrestsdk.Payment.find("PAY-57363176S1057143SKE2HO3A")

        if payment.execute({"payer_id": "DUFRQ8GWYMJXC"}):
            print("Payment execute successfully")
        else:
            print(payment.error) # Error Hash
        return Response()

class Cancel(APIView):
    def get(self,request):
        return Response({"message":"Payment Cancel"})