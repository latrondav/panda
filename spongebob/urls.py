from unicodedata import name
from django.urls import path

from django.contrib.auth import views as auth_views

from .import views

urlpatterns = [
    #main path
    path('', views.home_page),
    path('login/', views.login_page),
    path('signup/', views.signup_page),
    path('signout/', views.signout_page),
    path('activate/<uidb64>/<token>/', views.activate, name= "activate"),
    path('userview/', views.userview),
    path('findbus/', views.find_bus_page),
    path('contact_us/', views.contact_us_page),
    path('team/', views.team_page),
    path('bussearch/', views.bus_search_page),
    path('busbook/', views.bus_book_page),
    path('bookingdetails/', views.booking_details_page),
    path('bookings/', views.bookings_page),
    path('buses/', views.buses_page),
    path('addbus/', views.add_bus_page),
    path('busdetails/', views.bus_details_page),


    #reset password path
    path('resetpasswordform/', auth_views.PasswordResetView.as_view(template_name="password_mgt/pw_reset_form.html"), name= "password_reset_form"),
    path('resetpassworddone/', auth_views.PasswordResetDoneView.as_view(template_name="password_mgt/pw_reset_done.html"), name= "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_mgt/pw_reset_confirm.html"), name= "password_reset_confirm"),
    path('resetpasswordcomplete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_mgt/pw_reset_complete.html"), name= "password_reset_complete"),

    #change password path
    path('changepasswordform/', auth_views.PasswordChangeView.as_view(), name="password_change_form"),
    path('changepassworddone/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
]
