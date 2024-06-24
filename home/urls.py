from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views
urlpatterns = [
    # path('webhook', csrf_exempt(views.webhook_handler), name="webhook"),
    # path('verify/', views.verify_domain, name="verify"),
    # # path('', views.home, name="home")
    path('ezt_bot', csrf_exempt(views.processMessages), name="ezt_bot"),
    path('messenger_webhook', csrf_exempt(views.handle_messenger_webhook), name="messenger_webhook")
]
