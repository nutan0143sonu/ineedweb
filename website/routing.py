from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import *
from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<sender>[0-9A-Za-z_\-]+)/(?P<receiver>[0-9A-Za-z_\-]+)/(?P<applied_job_id>[0-9]+)$', ChatConsumer),
]
application = ProtocolTypeRouter({
  'websocket': AuthMiddlewareStack(
        URLRouter(
           websocket_urlpatterns
        )
    ),
})

