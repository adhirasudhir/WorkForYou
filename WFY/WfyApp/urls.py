from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('button/', views.Button, name='button'),
    path('profile/', views.Profile, name='profile'),
    path('after_profile/', views.after_profile, name='after-profile'),
    path('contact/', views.contact, name='contact'),
    path('Login/', views.Login, name='Login'),
    path('Register/', views.Register, name='Register'),
    path('Logout/', views.Logout, name='Logout'),
    path('activateuser/<uidb64>/<token>', views.ActivateUser, name='ActivateUser'),
    path('resetpassword/', auth_views.PasswordResetView.as_view(template_name='ResetPassword.html'),
         name='reset_password'),
    path('resetpassword/sent/', auth_views.PasswordResetDoneView.as_view(template_name='ResetPasswordSent.html'),
         name='password_reset_done'),
    path('resetpassword/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='ResetPasswordConfirm.html'),
         name='password_reset_confirm'),
    path('resetpassword/success/',
         auth_views.PasswordResetCompleteView.as_view(template_name='ResetPasswordSuccess.html'),
         name='password_reset_complete'),

    path('User/Dashboard', views.Dashboard, name='Dashboard'),

    #Devloper profile Access
    path('HTMLDeveloper/', views.Profile1, name='profile1'),
    path('JavaScriptDeveloper/', views.Profile2, name='profile2'),
    path('LaravelDeveloper/', views.Profile3, name='profile3'),
    path('PythonDeveloper/', views.Profile4, name='profile4'),
    path('PhpDeveloper/', views.Profile5, name='profile5'),
    path('MySQLDeveloper/', views.Profile6, name='profile6'),
    path('DjangoDeveloper/', views.Profile7, name='profile7'),
    path('BootstrapDeveloper/', views.Profile8, name='profile8'),
    path('MongoDBDeveloper/', views.Profile9, name='profile9'),
    path('contact/', views.contact, name='contact'),

]