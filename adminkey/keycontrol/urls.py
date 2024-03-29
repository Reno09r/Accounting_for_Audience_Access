from django.urls import path
from . import views

# Определение URL-маршрутов (urlpatterns) для приложения keycontrol.
urlpatterns = [
    path('', views.index, name='home'),
    path('tools/', views.tools, name='tools'),
    path('addemp/', views.addemp, name='addemp'),
    path('all_info/', views.all_info, name='all_info'),
    path('profile/', views.profile, name='profile'),
    path('roles_info/', views.roles_info, name='roles_info'),
    path('audience_info/', views.audience_info, name='audience_info'),
    path('schedule/', views.schedule, name='schedule'),
    path('mark_returned/', views.mark_returned, name='mark_returned'),
    path('mark_delete/', views.mark_delete, name='mark_delete'),
    path('upload/', views.upload, name='upload'),
    path('error/', views.error, name='error'),
    path('error/<str:error_msg>/', views.error, name='error_with_msg'),
]   
