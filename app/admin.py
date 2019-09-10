from django.contrib import admin
from django.utils.safestring import mark_safe
#from translations.admin import TranslatableAdmin, TranslationInline
from .models import *

#post api
#--------------------MyUser Admin--------------------------------------------
class MyUserAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">person_add</i>'
    list_display = ['id','email',
                    'is_active', 'last_login', 'action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'email', 'first_name','last_name')

    def action(self, obj):
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/myuser/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

    def save_model(self, request, obj, form, change):
        '''docstring'''
        if "password" in form.changed_data:
            formPassword = form.cleaned_data.get('password')
            obj.set_password(obj.password)
        obj.save()

admin.site.register(MyUser,MyUserAdmin)

#---------------------Personal Detail Admin----------------------------#
class PersonalDetailAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">local_library</i>'
    list_display = ['id','user','professional_title','action']
    list_display_links = None
    readonly_fields = []
    list_per_page = 50
    ordering = ('id',)
 
    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/personaldetailmodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/personaldetailmodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(PersonalDetailModel,PersonalDetailAdmin)


#get Api
#-----------------------Industry Admin----------------------------------
class IndustryModelAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">info</i>'
    list_display = ['id','industry_type','action']
    list_display_links = None
    readonly_fields = []
    list_per_page = 50
    ordering = ('id',)
 
    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/industrymodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/industrymodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(IndustryModel,IndustryModelAdmin)

#------------------------Area Admin---------------------------
class AreaAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">phonelink</i>'
    list_display = ('id','area','action')
    list_display_links = None
    list_per_page = 50
    ordering = ('id',)
 
    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/areamodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/areamodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(AreaModel,AreaAdmin)

#---------------------Tools And Language Admin------------------
class ToolsAndLanguageAdmin(admin.ModelAdmin):
    list_display = ('id','name','action')
    list_display_links = None
    list_per_page = 50
    ordering = ('id',)
 
    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/toolsandlanguagemodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/toolsandlanguagemodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(ToolsAndLanguageModel,ToolsAndLanguageAdmin)

#------------------------Speaking Language Admin--------------------
class SpeakingLanguageAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">spellcheck</i>'
    list_display = ('id','language_name','action')
    list_display_links = None
    list_per_page = 50
    ordering = ('id',)
 
    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/speakinglanguagemodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/speakinglanguagemodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(SpeakingLanguageModel,SpeakingLanguageAdmin)

#-----------------------Working Hour Admin---------------------
class WorkingHourAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">watch_later</i>'
    list_display = ('id','working_hour','action')
    list_display_links = None
    list_per_page = 50
    ordering = ('id',)
 
    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/workinghourmodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/workinghourmodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(WorkingHourModel,WorkingHourAdmin)


#user api
#-------------------User Industry Admin---------------
class UserIndustryAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">supervisor_account</i>'
    list_display = ('id','user','industry','action')
    list_display_links = None
    list_per_page = 50
    ordering = ('id',)
 
    def action(self, obj):
        return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/userindustrymodel/{}/change/'>View</a>".format(obj.id))
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/userindustrymodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(UserIndustryModel,UserIndustryAdmin)

#----------------------User Area Admin------------------
class UserAreaAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">supervisor_account</i>'
    list_display = ('id','user','area','action')
    list_display_links = None
    list_per_page = 50
    ordering = ('id',)
 
    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/userareamodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/userareamodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(UserAreaModel,UserAreaAdmin)

#--------------------User Tools And Language Admin-----------------------------------------
class UserToolsAndLanguageAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">supervisor_account</i>'
    list_display = ('id','user','skill','action')
    list_display_links = None
    list_per_page = 50
    ordering = ('id',)
 
    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/usertoolsandlanguagemodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/usertoolsandlanguagemodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(UserToolsAndLanguageModel,UserToolsAndLanguageAdmin)

#-----------------------------User Employee History Admin-------------------------------------
class UserEmploymentHistoryAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">supervisor_account</i>'
    list_display = ('id','user','designation','action')
    list_display_links = None
    list_per_page = 50
    ordering = ('id',)
 
    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/useremploymenthistorymodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/useremploymenthistorymodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(UserEmploymentHistoryModel,UserEmploymentHistoryAdmin)

#------------------------User Language Admin---------------------------------------------
class UserLanguageAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">supervisor_account</i>'
    list_display = ('id','user','userLanguage','action')
    list_display_links = None
    list_per_page = 50
    ordering = ('id',)
 
    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/userlanguagemodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/userlanguagemodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(UserLanguageModel,UserLanguageAdmin)


#---------------------Profession Admin--------------#
class ProfessionAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">work</i>'
    list_display = ['id', 'name','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)

    def action(self, obj):
    
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/profession/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/profession/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(Profession,ProfessionAdmin)

#----------------------------User Education Admin---------------------------------------
class UserEducationAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">wc</i>'
    list_display = ['id','user','schoolName','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'user','schoolName')

    def action(self, obj):
        # pass
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/usereducationmodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/app/usereducationmodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(UserEducationModel,UserEducationAdmin)