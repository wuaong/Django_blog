from django.urls import path
from user import views



urlpatterns=[
    path('login/',views.Login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('login_for_medal/',views.login_for_medal,name='login_for_medal'),
    path('register/',views.register,name='register'),
    path('user_info/',views.user_info,name='user_info'),
    path('change_nickname/',views.change_nickname,name='change_nickname'),
    path('change_password/',views.change_password,name='change_password'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('bind_Email/',views.bind_Email,name='bind_Email'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
]
