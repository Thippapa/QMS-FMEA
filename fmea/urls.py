from django.contrib import admin
from django.contrib import admin
from django.urls import path

from requirement import views

urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=False)),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('requirements/', views.requirement_list, name='requirement_list'),
    path('model-dashboard/', views.model_dashboard, name='model_dashboard'),
    path('approve-dashboard/', views.approve_dashboard, name='approve_dashboard'),
    path('cp-form/', views.cp_form, name='cp_form'),
]