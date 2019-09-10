from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import *

app_name = 'application'
urlpatterns = [
    url(r'^login/$', LoginView.as_view()),
    url(r'^forgot/$', ForgotPaswordView.as_view()),
    url(r'^otp-verify/$', OtpVerficationView.as_view()),
    url(r'^reset-password/$', ResetPasswordView.as_view()),
    url(r'^image-upload/$', ImageUploadView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)