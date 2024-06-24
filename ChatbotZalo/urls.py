from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('webhook', csrf_exempt(views.webhook_handler), name="zalo_webhook")
]