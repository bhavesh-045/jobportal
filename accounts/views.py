from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import StudentSignUpForm,RecruiterForm,ProfileEditForm
from .models import CustomUser
from django.db.models import Count
from jobs.models import Job,JobApplication

# Create your views here.

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,'Student Registered Successfully')
            return redirect('student_dashboard')
        else:
            messages.error(request,"Please correct the highlighted errors.")
    else:
        form = StudentSignUpForm()

    return render(request,'accounts/signup.html',{'form_data':form,'user_type': 'Student'})         




def recruiter_signup(request):
    if request.method == 'POST':
        form = RecruiterForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,'Recruiter Registered Successfully')
            return redirect('recruiter_dashboard')
        else:
            messages.error(request,"Please correct the highlighted errors.")
    else:
        form = RecruiterForm()

    return render(request,'accounts/signup.html',{'form_data':form,'user_type': 'Recruiter'}) 



def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = CustomUser.objects.get(email=email)
            user = authenticate(request,username=user_obj.email,password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request,user)

            if user.role == 'student':
                messages.success(request,'Student Logged Successfully')
                return redirect('student_dashboard')
            elif user.role == 'recruiter':
                messages.success(request,'Recruiter Logged Successfully')
                return redirect('recruiter_dashboard')
            else:
                return redirect('admin:index')
        else:
            messages.error(request,'Invalid Email or Password.')

    return render (request,'accounts/login.html')  


@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def student_dashboard(request):
    user = request.user 
    total_jobs = Job.objects.count()
    jobs_applied = JobApplication.objects.filter(student=user).count()
    job_type_data =(
        Job.objects.values('job_type').annotate(count=Count('job_type')).order_by('-count')
    )
    applications = JobApplication.objects.filter(student=request.user)
    unseen_count = applications.filter(status_notified=True).exclude(status='applied').count()

    chart_labels = [item['job_type'] for item in job_type_data]
    chart_data = [item['count'] for item in job_type_data]
    return render(request,'accounts/student_dashboard.html',{
        'total_jobs':total_jobs,
        'jobs_applied':jobs_applied,
        'chart_labels':chart_labels,
        'chart_data':chart_data,
        'applications':applications,
        'unseen_count':unseen_count
    })
          

@login_required
def recruiter_dashboard(request):
    user = request.user
    jobs = Job.objects.filter(posted_by=user)
    total_jobs = jobs.count()
    total_applications = JobApplication.objects.filter(jobs__posted_by=user).count()
    most_applied_job = (
        jobs.annotate(app_count=Count('jobapplication')).order_by('-app_count').first()
    )

    chart_labels = []
    chart_data = []
    for job in jobs:
        chart_labels.append(job.title)
        chart_data.append(job.jobapplication_set.count())


    context = {
        'total_jobs':total_jobs,
        'total_applications':total_applications,
        'most_applied_job':most_applied_job,
        'recent_jobs':jobs.order_by('-created_at')[:5],
        'chart_labels':chart_labels,
        'chart_data':chart_data
    }
    return render(request,'accounts/recruiter_dashboard.html',context)   


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST,request.FILES,instance=user,user=user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Updated Successfully')
            if user.role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('recruiter_dashboard')
        else:
            messages.error(request,'Some Issue in Updating')
    else:
        form = ProfileEditForm(instance=user,user=user)
    return render(request,'accounts/edit_profile.html',{'form':form})


@login_required
def student_applied_jobs(request):
     applications = JobApplication.objects.filter(student=request.user)
     applications.filter(status_notified=True).exclude(status='applied').update(status_notified=False)
     return render(request,'accounts/student_applied_jobs.html',{'applications':applications})