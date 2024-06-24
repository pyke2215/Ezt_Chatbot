from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views
urlpatterns = [
    path('webhook', views.handle_messenger_webhook, name="messenger_webhook")
]
