import os
import time
import ast
from datetime import date, timedelta
import datetime


from app.models import *
from website.models import *
from rest_framework.response import Response
from .serializers import *
from django.db.models import Q
import json

def jobfiltering(instance,params):
    """Toal filtering foe job section only"""
    
    if 'duration' in params and params['duration']:
        instance=instance.filter(duration=params['duration'])
    if 'type_of_project' in params and params['type_of_project']:
        instance=instance.filter(type_of_project=params['type_of_project'])
    if 'salary' in params and params['salary']:
        instance=instance.filter(desiredSalary__salaryPerHour=params['salary'])
    if 'posted_date' in params and params['posted_date']:
        import datetime
        current = datetime.datetime.now().date()
        if params['posted_date'] == "today":
            instance = instance.filter(
                created_at__date=current
            )
        elif params['posted_date'] == "yesterday":
            instance = instance.filter(
                created_at__date=current - timedelta(1)
            )
        elif params['posted_date'] == "week":
            current = current - timedelta(7)
            weekday = current.weekday()
            start_delta = datetime.timedelta(days=weekday)
            start = current - start_delta
            end = start + datetime.timedelta(days=6)
            instance = instance.filter(
                created_at__date__gte=start,
                created_at__date__lt=end
            )
            print(instance)
        elif params['posted_date'] == "month":
            end = current.replace(day=1)
            print("end",end)
            end = end - timedelta(days=1)
            print("end",end)
            start = end.replace(day=1)
            print("start",start)
            instance = instance.filter(
                created_at__date__gte=start,
                created_at__date__lt=end
            )
    if "search" in params and params['search']:
        area=PostJobAreaModel.objects.filter(area__area__icontains=params['search']).values_list('job__id',flat=True)
        posted_skills = PostJobSkillModel.objects.filter(skills__name__icontains=params['search']).values_list('job__id',flat=True)
        posted_location = PostJobPreferenceLocationModel.objects.filter(preferenceLocation__locationName__icontains=params['search']).values_list('job__id',flat=True)
        posted_language = PostJobPreferenceLanguageModel.objects.filter(preferenceLanguage__language_name__icontains=params['search']).values_list('job__id',flat=True)
        instance = instance.filter(
            Q(jobTitle__icontains=params['search']) | Q(user__first_name__icontains=params['search']) | Q(type_of_project__icontains=params['search'])\
            | Q(desiredSalary__salaryPerHour__icontains=params['search']) |Q(id__in=area) | Q(id__in=posted_skills) | Q(id__in=posted_language) | Q(id__in=posted_location))
    return instance

def userfiltering(instance,params):
    """Searchig for user detail filtering"""
    if "search" in params and params['search']:
        persional_detail = PersonalDetailModel.objects.filter(
            Q(timezone=params['search']) | Q(country=params['search']) | Q(city=params['search']) | Q(professional_title=params['search'])\
            | Q(work_hour__working_hour__icontains=params['search'])
            ).values_list("user__id",flat=True)
        user_industry = UserIndustryModel.objects.filter(industry__industry_type__icontains=params['search']).values_list("user__id",flat=True)
        user_area = UserAreaModel.objects.filter(area__area__icontains=params['search']).values_list("user__id",flat=True)
        user_skill = UserToolsAndLanguageModel.objects.filter(skill__name__icontains=params['search']).values_list("user__id",flat=True)
        user_language = UserLanguageModel.objects.filter(userLanguage__language_name__icontains=params['search']).values_list('user__id',flat=True)
        user_education = UserEducationModel.objects.filter(
            Q(schoolName__icontains=params['search']) | Q(university_name__icontains=params['search']) | Q(board__icontains=params['search'])\
            | Q(percentage__icontains=params['search']) | Q(yos=params['search']) | Q(yop=params['search']) | Q(course=params['search']) |\
            Q(stream__icontains=params['search'])
        ).values_list("user__id",flat=True)
        user_employement = UserEmploymentHistoryModel.objects.filter(
            Q(company_name__icontains=params['search']) | Q(designation__icontains=params['search'])
        ).values_list("user__id",flat=True)
        instance = instance.filter(
            Q(email__icontains=params['search']) | Q(first_name__icontains=params['search']) | Q(last_name__icontains=params['search'])\
            | Q(id__in=user_industry) | Q(id__in=user_area) | Q(id__in=user_skill) | Q(id__in=persional_detail) | Q(id__in=user_language)\
            | Q(id__in=user_education) | Q(id__in=user_employement)
        )
    return instance
def matchingJobfilter(request,job_id,context):
    """Filter for Job Seeker"""
    params=request.GET
    if context == 'activeJob':
        instance = JobManagement.objects.filter(id__in=job_id)
    elif context=='favoriteJob':
        instance = JobManagement.objects.filter(id__in=job_id)
    elif context=='userApplyJob':
        instance = JobManagement.objects.filter(id__in=job_id)
    elif context =='userMatchigngJob':
        instance = JobManagement.objects.filter(id__in=job_id,is_active=True)
    elif context == 'completedJob':
        instance = JobManagement.objects.filter(id__in=job_id)
    elif context =='pendingJob':
        instance = JobManagement.objects.filter(id__in=job_id)
    elif context == 'getPostedJob':
        instance = JobManagement.objects.filter(user=request.user)
    elif context == 'employerJobApplicant':
        instance = JobManagement.objects.filter(id__in=job_id)
    elif context == 'employerCompletedJob':
        instance = JobManagement.objects.filter(id__in=job_id)
    data = jobfiltering(instance,params)
    return data

def LookingForJob(request):
    """Looking for Job"""
    params=request.GET
    instance = JobManagement.objects.filter(is_active=True)
    data = jobfiltering(instance,params)
    return data

def applicantFilter(request,job):
    """Applicant Filter function"""
    # print(instance,request.user,job)
    params = request.GET
    instance = MyUser.objects.filter(email__in=job)
    data = userfiltering(instance,params)  
    return data           
           
def employerActiveJobFilter(request,user_applied_job):
    """Filtering for employer active job"""
    params = request.GET
    job_id = user_applied_job.values_list("job__id",flat=True).distinct("job__id")
    user_id = user_applied_job.values_list("user__id",flat=True).distinct("user__id")
    applied_user = MyUser.objects.filter(id__in=user_id)
    job_instance = request.user.company.filter(id__in=job_id)
    user_filter = userfiltering(applied_user,params)
    job_filter = jobfiltering(job_instance,params)
    instance = user_applied_job.filter(Q(user__in=user_filter) | Q(job__in=job_filter))
    return instance

        
