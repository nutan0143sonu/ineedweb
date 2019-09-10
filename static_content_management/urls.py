from django.conf.urls import url

from .views import *


app_name = 'static-content'
urlpatterns = [
    url(r"^about-us$",AboutUsView.as_view()),
    url(r"^term-and-condition$",TermAndConditionView.as_view()),
    url(r"^contact-us$",ContactUsView.as_view()),
    url(r"^faq$",FAQView.as_view()),
    url(r"^privacy-policy$",PolicyPrivacyView.as_view()),
    url(r"^career$",CareersView.as_view()),
    url(r"^resume-upload$",ResumeUploadView.as_view()),
    url(r"^whoiam$",WhoIAmView.as_view()),


]
