from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000
    path('mark_returned/', views.mark_returned, name='mark_returned'),
    path('tools/', views.tools, name='tools'),
    path('addemp/', views.addemp, name='addemp'),
    path('all_info/', views.all_info, name='all_info'),
    path('profile/', views.profile, name='profile'),
    path('roles_info/', views.roles_info, name='roles_info'),
    path('audience_info/', views.audience_info, name='audience_info'),
]
