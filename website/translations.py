from app.models import *
from website.models import *
from googletrans import Translator
translator = Translator()

#---------Industry translation----------------------------
def industryTranslation(user,language):
    """Translation fuction of industry  data from english ro franch language."""
    industry1 = UserIndustryModel.objects.filter(user=user)
    my_list = []
    for data in industry1:
        my_dict={'industry_type':translator.translate(data.industry.industry_type,language).text}
        my_list.append(my_dict)
    return my_list

#------------------------area tanslation---------------------------------
def areaTranslation(user,language):
    """Translation fuction of area  data from english ro franch language."""
    area = UserAreaModel.objects.filter(user=user)
    my_list = []
    for data in area:
        my_dict={'area':translator.translate(data.area.area,language).text}
        my_list.append(my_dict)
    return my_list

def skillTranslation(user,language):
    """Translation fuction of skill  data from english ro franch language."""
    skill = UserToolsAndLanguageModel.objects.filter(user=user)
    my_list = []
    for data in skill:
        my_dict={'skill':translator.translate(data.skill.name,language).text,"rating":data.rating}
        my_list.append(my_dict)
    return my_list
#-------------User Language translation---------------------
def languageTranslation(user,language):
    """Translation fuction of speaking language  data from english ro franch language."""
    lan = UserLanguageModel.objects.filter(user=user)
    my_list = []
    for data in lang:
        my_dict={'language':translator.translate(data.userLanguage.language_name,language).text,'rating':data.rating}
        my_list.append(my_dict)
    return my_list

#--------------Education data------------------------
def EducationTranslation(user,language):
    """Translation Education of Job Seeker from one language to another langyage"""
    edu = UserEducationModel.objects.filter(user=user)
    my_list = []
    for data in lang:
        my_dict={
            'schoolName':translator.translate(data.schoolName,language).text,
            'university_name':translator.translate(data.university_name,language).text,
            'board':translator.translate(data.board,language).text,
            'percentage':data.percentage,
            'yos':data.yos,
            'yop':data.yop,
            'course':translator.translate(data.course,language).text,
            'stream':translator.translate(data.stream,language).text,
            'activity':translator.translate(data.activity,language).text,
            'description':translator.translate(data.description,language).text,     
            }
        my_list.append(my_dict)
    return my_list

#-------------Personal Detail------------------------------------
def personalDetailTranslation(user,language):
    """Job Seeker Personal data is translated form one languae to another"""
    personal = PersonalDetailModel.objects.get(user=user)
    my_dict={
        'id':personal.id,
        'working_hour':translator.translate(personal.work_hour.working_hour,language).text,
        'professional_title':translator.translate(personal.professional_title,language).text,
        'professional_description':translator.translate(personal.professional_description,language).text,
        'paypal_account_id':translator.translate(personal.paypal_account_id,language).text,
        'country':translator.translate(personal.country,language).text,
        'timezone':translator.translate(personal.timezone,language).text,
        'postal_code':translator.translate(personal.postal_code,language).text,
        'city':translator.translate(personal.city,language).text,
        'mobile':translator.translate(personal.mobile,language).text
        }
    return my_dict

    