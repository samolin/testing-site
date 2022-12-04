from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
]