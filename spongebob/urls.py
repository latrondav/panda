from django.urls import path
from django.urls import URLPattern
from .import views

urlpatterns = [
    #path('hello/', views.home),
    path('', views.home_page),
    path('signout/index/', views.home_page),
    path('login/', views.login_page),
    path('login/log/', views.login_page),
    path('sign up/login/', views.login_page),
    path('sign up/', views.signup_page),
    path('sign up/sign/', views.signup_page),
    path('sign up/index/', views.signup_page),
    path('signout/', views.signout_page),
    path('activate/<uidb64>/<token>/', views.activate, name= "activate"),
    path('trinity home/', views.trinity_home_page),
    path('trinity book/', views.trinity_book_page),
    path('services/', views.services_page),
    path('services/index/', views.home_page),
    path('contact_us/', views.contact_us_page),
    path('team/', views.team_page),
]
