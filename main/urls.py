from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.home, name='home'),
    path('verify/', views.verifyUser, name='verifyUser'),
    path('upload/', views.upload_file, name='upload'),
    path('download/', views.download_data, name='download'),
]