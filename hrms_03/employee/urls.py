from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('emp_home', views.emp_home, name='emp_home'),
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('leaveApply', views.leaveApply, name='leaveApply'),
    path('deleteLeave/<id>/', views.deleteLeave, name='deleteLeave'),
]