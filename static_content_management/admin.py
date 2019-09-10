from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

#-------------------------Conact Us Admin-------------------------------------------------------------------------------------------------
class ContactUsAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_circle</i>'
    list_display = ['id','email', 'action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'email', 'mobile','address')

    def action(self, obj):
        view="<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/contactus/{}/change/'>View</a>".format(obj.id)
        delete="<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/contactus/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))
admin.site.register(ContactUS,ContactUsAdmin)

#-------------------------------------FAQ Admin---------------------------------------------------------------------------------------------
class FAQAdmin(admin.ModelAdmin):
    list_display = ['id','question', 'action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'question')

    def action(self, obj):
        view="<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/faq/{}/change/'>View</a>".format(obj.id)
        delete="<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/faq/{}/delete/'>Delete</a>".format(obj.id)        
        return mark_safe("%s <b> %s <b>" %(delete,view))
admin.site.register(FAQ,FAQAdmin)

#-------------------------About Us Admin-------------------------------------------------------------------------------------------------------------------
class AboutUSdmin(admin.ModelAdmin):
    list_display = ['id','title','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'title')

    def action(self, obj):
        # pass
        view="<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/aboutus/{}/change/'>View</a>".format(obj.id)
        delete="<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/aboutus/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))
admin.site.register(AboutUs,AboutUSdmin)

#-------------------------------------Term and Condition Admin-------------------------------------------------------------------------------
class TermAndConditionAdmin(admin.ModelAdmin):
    list_display = ['id','title','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'title')

    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/termsandconditions/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/termsandconditions/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))
admin.site.register(TermsAndConditions,TermAndConditionAdmin)

#-------------------------------------Privacy Policy Admin-------------------------------------------------------------------------------
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['id','title','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'title')

    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/privacypolicy/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/privacypolicy/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

admin.site.register(PrivacyPolicy,PrivacyPolicyAdmin)

#---------------------------------Career Admin---------------------------------------------------------------------------------------------
class DontLog:
    def log_addition(self, *args):
        return False
class CareerAdmin(DontLog,admin.ModelAdmin):
    icon='<i class="material-icons">work</i>'
    list_display = ['id','email','profession','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('updated_at',)
    search_fields = ('id', 'email')

    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/career/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/career/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]
        
    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return False
        return super(CareerAdmin, self).has_change_permission(request, obj)
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Career,CareerAdmin)

#----------------------Notification-----------------------------------------
class WhoIAmAdmin(admin.ModelAdmin):
    list_display = ['id','title','action']
    list_display_links = None
    list_per_page = 50
    readonly_fields = []
    ordering = ('id',)
    search_fields = ('id', 'title')

    def action(self, obj):
        view = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/whoiam/{}/change/'>View</a>".format(obj.id)
        delete = "<a class='button btn' style='color:white; padding:0 1rem;' href='/admin/static_content_management/whoiam/{}/delete/'>Delete</a>".format(obj.id)
        return mark_safe("%s <b> %s <b>" %(delete,view))
admin.site.register(WhoIAm, WhoIAmAdmin)