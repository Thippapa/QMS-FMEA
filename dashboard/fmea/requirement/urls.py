from django.urls import path
from . import views

urlpatterns = [
    path('', views.requirement_list, name='requirement_list'),
    path('model-dashboard/', views.model_dashboard, name='model_dashboard'),
]