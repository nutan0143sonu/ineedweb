from django.contrib import admin
from django.conf.urls import url,include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('website.urls', namespace='website')),
    url(r'^api/', include('app.urls', namespace='application')),
    url(r'^static-content/', include('static_content_management.urls', namespace='static-content')),
    url(r'^djrichtextfield/', include('djrichtextfield.urls')),
]
