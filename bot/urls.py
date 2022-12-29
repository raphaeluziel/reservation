from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('chatbot', views.chatbot, name='chatbot'),
]