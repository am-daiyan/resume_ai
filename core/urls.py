from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms, name='terms'),
    path('FAQs/', views.FAQs, name='FAQs'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('list/', views.list, name='list'),
    path('logout/', views.user_logout, name='user_logout'),
    path('rough/', views.rough, name='rough'),
    path('student_d/', views.student_d, name='student_d'),
    path('preview/<int:id>/', views.preview, name='preview'),

]