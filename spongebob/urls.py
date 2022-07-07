from django.urls import path

from django.contrib.auth import views as auth_views

from .import views

urlpatterns = [
    #path('hello/', views.home),
    path('', views.home_page),
    path('login/', views.login_page),
    path('signup/', views.signup_page),
    path('signout/', views.signout_page),
    path('activate/<uidb64>/<token>/', views.activate, name= "activate"),
    path('trinity home/', views.trinity_home_page),
    path('trinity book/', views.trinity_book_page),
    path('services/', views.services_page),
    path('contact_us/', views.contact_us_page),
    path('team/', views.team_page),

    #forget password path
    path('resetpassword/', auth_views.PasswordResetView.as_view(), name= "reset_password"),
    path('resetpasswordsent/', auth_views.PasswordResetDoneView.as_view(), name= "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name= "password_reset_confirm"),
    path('resetpasswordcomplete/', auth_views.PasswordResetCompleteView.as_view(), name= "password_reset_complete"),

]
