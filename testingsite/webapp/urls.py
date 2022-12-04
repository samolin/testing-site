from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.TestListView.as_view(), name='home'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<slug:test_name>/', views.answer_home, name='answerDetails')
]
