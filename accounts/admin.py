from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from jobs.models import Job,JobApplication

# Register your models here.

@admin.register(CustomUser)
class CustomUseAdmin(admin.ModelAdmin):
    list_display = ('email','full_name','role','is_active','is_staff')
    list_filter = ('role','is_active')
    search_fields =('email','full_name')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title','company','location','job_type','deadline','created_at')
    list_filter = ('job_type','created_at','company')
    search_fields =('title','comapny','location')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('student','jobs','applied_at','status')
    list_filter = ('status','applied_at')
    search_fields =('student__email','jobs__title')