from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

#----------------------Notification-----------------------------------------
class NotificationAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">notifications</i>'
    list_display = ['id','title','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'title')

    def action(self, obj):
        # pass
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/notification/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/notification/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(Notification,NotificationAdmin)

#-------------------------Location Admin----------------------------------------
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id','locationName','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'locationName')

    def action(self, obj):
        # pass
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/location/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/location/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(Location,LocationAdmin)

#-------------------------------Salary Per Hour Admin----------------------------------
class SalaryPerHourAdmin(admin.ModelAdmin):
    list_display = ['id','salaryPerHour','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'salaryPerHour')

    def action(self, obj):
        # pass
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/salary/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/salary/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(Salary,SalaryPerHourAdmin)

#-----------------Job Post Management----------------------------------------------------
class JobManagementAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">wc</i>'
    list_display = ['id','jobTitle','user','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'jobTitle','user')

    def action(self, obj):
        # pass
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/jobmanagement/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/jobmanagement/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(JobManagement,JobManagementAdmin)

# #-------------------Post Job Area Admin----------------------------------------------
class PostJobAreaAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">wc</i>'
    list_display = ['id','job','area','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'job','area')

    def action(self, obj):
        # pass
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/postjobareamodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/postjobareamodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(PostJobAreaModel,PostJobAreaAdmin)

#---------------------Post Job Skill Admin---------------------------------------------
class PostJobSkillAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">wc</i>'
    list_display = ['id','job','skills','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'job','skills')

    def action(self, obj):
        # pass
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/postjobskillmodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/postjobskillmodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(PostJobSkillModel,PostJobSkillAdmin)

#----------------------Post Job PreferenceLanguage Admin-----------------------------------
class PostJobPreferenceLanguageAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">wc</i>'
    list_display = ['id','job','preferenceLanguage','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'job','preferenceLanguage')

    def action(self, obj):
        # pass
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/postjobpreferencelanguagemodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/postjobpreferencelanguagemodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(PostJobPreferenceLanguageModel,PostJobPreferenceLanguageAdmin)

#-----------------------Post Job PreferenceLocation Admin--------------------------------
class PostJobPreferenceLocationAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">wc</i>'
    list_display = ['id','job','preferenceLocation','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'job','preferenceLocation')

    def action(self, obj):
        # pass
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/postjobpreferencelocationmodels/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/postjobpreferencelocationmodels/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(PostJobPreferenceLocationModel,PostJobPreferenceLocationAdmin)

 #---------------------User Apply Job Admin---------------------------------------------
 
class UserApplyJobAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">wc</i>'
    list_display = ['id','job','user','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'job','user')

    def action(self, obj):
        # pass
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/userapplyjob/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/userapplyjob/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(UserApplyJob,UserApplyJobAdmin)

#----------------------Chat Model Admin--------------------------------------------------------

class ChatModelAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">wc</i>'
    list_display = ['id','sender','receiver','created_at','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'job','user')

    def action(self, obj):
        
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/chatmodel/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/chatmodel/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(ChatModel,ChatModelAdmin)

#-------------------------------Review Rating Admin-------------------------------------------

class ReviewAndRatingAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">wc</i>'
    list_display = ['id','receiver_user','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'receiver_user')

    def action(self, obj):
        
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/reviewandrating/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/reviewandrating/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(ReviewAndRating,ReviewAndRatingAdmin)

#---------------------------------------User Reference Admin ---------------------------------------

class UserReferenceAdmin(admin.ModelAdmin):
    icon='<i class="material-icons">wc</i>'
    list_display = ['id','sender','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    search_fields = ('id', 'sender')

    def action(self, obj):
        
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/userreference/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/website/userreference/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(UserReference,UserReferenceAdmin)