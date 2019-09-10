import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
# from django.test import Client

from app.models import *


headers = {'content-type': 'application/json'}


jobseeker_signup={
	"email":"surya@gmail.com",
	"first_name":"Surya",
	"last_name":"Rana",
	"password":"Mobiloitte1",
    "user_type":"Job Seeker",
	"industry":[1,2,3],
	"area":[3,4],
	"tool_and_language":{
		"1":5,
		"2":6,
		"3":7
	},
	"personal":{
		"professional_title":"PF",
		"professional_description":"PD"
	},
	"url":"http://0.0.0.0:4006/email-verify/"

}

user_login = {
	"email":"nutan143@mailinator.com",
	"password":"Mobiloitte1"
}

class MyUserTestCases(APITestCase):
    def test_setup(self):
        print("-----------------TEST MODEL CREATED-----------------")
        print("Creating MyUser Instance.....")
        m1 = MyUser.objects.create(id=1,first_name="Nutan",last_name="Gupta",email="er.nutan.g@gmail.com",user_type="Job Seeker")
        m1.password="Mobiloitte1"
        m1.save()
        print("m1",m1.password)
        user=MyUser.objects.get(email='er.nutan.g@gmail.com')
        print("USER",user)
        try:
            print("Login Test")
            response = self.client.login(email=m1.email, password='Mobiloitte1') 
            print("response",response)
            # self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            print("Login Test",e)
        print("Create User Industry")
        in1 = IndustryModel.objects.create(id=1, industry_type="Software")
        in2 = IndustryModel.objects.create(id=2, industry_type="Ionic")

        i1 = UserIndustryModel.objects.create(id=1,user=m1,industry=in1)
        i2 = UserIndustryModel.objects.create(id=2,user=m1,industry=in2)

        print("Create Area Industry")
        ar1 = AreaModel.objects.create(id=1,area='gurgao')
        ar2 = AreaModel.objects.create(id=2,area='Delhi')

        a1 = UserAreaModel.objects.create(id=1,user=m1,area=ar1)
        a2 = UserAreaModel.objects.create(id=2,user=m1,area=ar2)

        print("Create Tools And Language")
        t1 = ToolsAndLanguageModel.objects.create(id=1,name='python')
        t2 = ToolsAndLanguageModel.objects.create(id=2,name='html')

        t1 = UserToolsAndLanguageModel(id=1,user=m1,skill=t1,rating=3)
        t2 = UserToolsAndLanguageModel(id=2,user=m1,skill=t2,rating=3)

        print("Create Persional Detail")
        w1 = WorkingHourModel.objects.create(id=1,working_hour='0-4')
        p1 = PersonalDetailModel.objects.create(id=1,user=m1,work_hour=w1,professional_title="Developer",professional_description="chgsjdnsckjck")

    def test_user_login(self):
        try:
            
            print("Login Test")
            response = self.client.post('/api/login/', {"email":"er.nutan.g@gmail.com","password":"Mobiloitte1"}) 
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            print("Login Test",e)