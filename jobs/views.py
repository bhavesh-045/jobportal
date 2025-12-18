from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
from .models import Job,JobApplication,APPLICATION_STATUS_CHOICES
from django.contrib import messages

# Create your views here.

@login_required
def job_create(request):
    if not request.user.role == 'recruiter':
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request,'Job Posted Successfully')
            return redirect('recruiter_dashboard')
    else:
        form = JobPostForm()
    return render(request,'jobs/jobs_create.html',{'form_data':form})  

@login_required
def recruiter_job(request):
     if not request.user.role == 'recruiter':
         return redirect('student_dashboard')
     
     jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
     return render(request,'jobs/recruiter_jobs.html',{'jobs':jobs})

def view_all_job(request):
    if not request.user.role == 'student':
        return redirect('recruiter_dashboard')
    job_data = Job.objects.all()
    return render(request,'accounts/view_all_jobs.html',{'job_key':job_data})      

def job_detail(request,id):
    job = get_object_or_404(Job,id=id)
    return render(request,'jobs/job_detail.html',{'job_all':job})

def apply_job(request,id):
    if not request.user.is_authenticated or not request.user.role == 'student':
        messages.error(request,"Only Students can Apply.")
        return redirect('login')
    
    job = get_object_or_404(Job,id=id)
    already_applied = JobApplication.objects.filter(jobs=job,student=request.user).exists()
    if already_applied:
        messages.warning(request,"You have Already Apllied for this Job")
    else:
        JobApplication.objects.create(jobs=job,student=request.user)
        messages.success(request,"Successfully Applied to the Job")
    return redirect('job_detail',id=id)   


@login_required
def edit_job(request,job_id):
    job = get_object_or_404(Job,id=job_id,posted_by=request.user)
    if request.method == 'POST':
        form = JobPostForm(request.POST,instance=job)
        if form.is_valid():
            form.save()
            messages.success(request,'Job Updated Successfully')
            return redirect('recruiter_dashboard')
    else:
        form = JobPostForm(instance=job)
    return render(request,'jobs/edit_job.html',{'form_data':form})


@login_required
def delete_job(request,job_id):
    job = get_object_or_404(Job,id=job_id,posted_by=request.user)
    if request.method == 'POST':
        job.delete()
        messages.info(request,'Job Deleted Successfully')
        return redirect('recruiter_dashboard')
    return render(request,'accounts/recruiter_jobs.html',{'job_key':job}) 


@login_required
def view_applicants(request,job_id):
    job = get_object_or_404(Job,id=job_id,posted_by=request.user)
    applications = JobApplication.objects.filter(jobs=job).select_related('student')
    return render(request,'jobs/view_applicants.html',{'job':job,'applications':applications,'status_choices':APPLICATION_STATUS_CHOICES})

@login_required
def update_applications_status(request,application_id):
    if request.method == 'POST':
        application = get_object_or_404(JobApplication,id=application_id)
        new_status = request.POST.get('status')
        if new_status in dict(APPLICATION_STATUS_CHOICES):
            application.status = new_status
            application.satus_notified = False
            application.save()
            messages.success(request,f"Application Status updated to {new_status.title()} Successfully")
        else:
            messages.error(request,'Invalid Status Provided')
        return redirect('view_applicants',job_id=application.jobs.id)