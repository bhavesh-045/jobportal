from django.urls import path
from . import api_views

urlpatterns = [
    path('jobs/',api_views.job_list_view,name='job_list_api'),
    path('jobs/<int:id>/',api_views.job_detail,name='job_detail'),
    path('job_create/',api_views.job_create1,name='job_create1'),
    path('job_update/<int:id>/',api_views.job_update,name='job_update'),
    path('job_delete/<int:id>/',api_views.job_delete,name='job_delete'),

]