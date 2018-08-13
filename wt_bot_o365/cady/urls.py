from django.urls import path, re_path
from cady import views

urlpatterns = [
    path('api/dialogflow', views.dialogflow),
    re_path(r'^authorize', views.authorize),
    re_path(r'^token', views.token),
]
