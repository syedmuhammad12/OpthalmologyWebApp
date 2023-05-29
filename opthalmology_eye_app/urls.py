from django.contrib import admin
from django.urls import path, include
from opthalmology_eye_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('modelspage', views.models_page, name="models_page"),
    path('modelspageredirect', views.models_page_redirect, name="models_page_redirect"),
    path('model1page', views.model1_page, name="model1_page"),
    path('model2page', views.model2_page, name="model2_page"),
    path('model3page', views.model3_page, name="model3_page"),
    path('registraionpage', views.registration_page, name="registration_page"),
    path('reportpage', views.report_page, name="report_page"),
    path('model_eval', views.model_eval, name="model_eval"),
    path('logout', views.logout, name="logout"),
]