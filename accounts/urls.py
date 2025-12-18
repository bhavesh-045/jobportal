from django.urls import path 
from .import views

urlpatterns = [
    path('signup/student/',views.student_signup,name='student_signup'),
    path('signup/recruiter/',views.recruiter_signup,name='recruiter_signup'),
    path('login/',views.custom_login,name='login'),
    path('logout/',views.custom_logout,name='logout'),
    path('student/dashboard',views.student_dashboard,name='student_dashboard'),
    path('recruiter/dashboard',views.recruiter_dashboard,name='recruiter_dashboard'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('student/applications/',views.student_applied_jobs,name='student_applied_jobs'),
    ]