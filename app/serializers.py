from .models import *

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField



#------------Industry Serializer---------------------
class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryModel
        fields = '__all__'
#---------------Area serializer----------------------
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaModel
        fields = '__all__'
#---------------Tool and
class ToolsAndLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolsAndLanguageModel
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields =  ("email",)



class UserAreaSerializer(serializers.ModelSerializer):
    area_name = AreaSerializer(read_only=True, many=True)
    name = SerializerMethodField()
    def get_name(self,obj):
        if obj.area:
            return obj.area.area
    class Meta:
        model = UserAreaModel
        exclude = ('user','area')

class UserIndustrySerializer(serializers.ModelSerializer):
    industry_name = IndustrySerializer(read_only=True, many=True)
    name = SerializerMethodField()

    def get_name(self, obj):
        if obj.industry:
            return obj.industry.industry_type

    class Meta:
        model = UserIndustryModel
        exclude = ('user','industry')
class UserToolAndLanguageserializer(serializers.ModelSerializer):
    skill_name = ToolsAndLanguageSerializer(read_only=True, many=True)
    name = SerializerMethodField()

    def get_name(self, obj):
        if obj.skill:
            return obj.skill.name
    class Meta:
        model = UserToolsAndLanguageModel
        exclude = ('user','skill')

class UserpersonalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetailModel
        exclude = ('user','id')

#----------User Serializer------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    user_industry = UserIndustrySerializer(read_only=True, many=True)
    user_area = UserAreaSerializer(read_only=True, many=True)
    user_personal_detail = UserpersonalDetailSerializer(read_only=True)
    user_skill = UserToolAndLanguageserializer(read_only=True, many=True)
    class Meta:
        model = MyUser
        exclude = ('password','last_login','is_superuser','uuid','is_active',
                   'is_staff','created_at','updated_at','user_permissions','groups','otp')
