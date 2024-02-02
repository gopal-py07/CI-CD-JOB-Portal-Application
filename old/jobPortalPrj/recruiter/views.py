from django.shortcuts import render,redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Job, Selected, Applicants
from django.contrib.auth.decorators import login_required
from .forms import NewJobForm
from django.contrib import messages
from candidates.models import Profile
from users.decortor import *
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
# Create your views here.

def getJob_list(request):
    
    jobs = Job.objects.filter(recruiter=request.user).order_by('-date_posted')
    paginator = Paginator(jobs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'manage_jobs_page': "active",
        'jobs': page_obj,
        'rec_navbar': 1,
    }
    return render(request, 'recruiter/listJobs.html', context)


@user_passes_test(is_recruiter)
def add_job(request):
    
    user = request.user
    
    if request.method == "POST":
        form = NewJobForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.recruiter = user
            data.save()
            return redirect('recruiter:listJobs')
    else:
        form = NewJobForm()
    context = {
        'add_job_page': "active",
        'form': form,
        'rec_navbar': 1,
    }
    return render(request, 'recruiter/add_job.html', context)


def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
  
    context = {
        'job': job,
        'rec_navbar': 1,
    }
    
    return render(request, 'recruiter/job_detail.html', context)


def get_rec_details(request):
 
   
    context = {
        'rec_home_page': "active",
        'rec_navbar': 1,
    }
    return render(request, 'recruiter/rec_details.html', context)


@login_required
@user_passes_test(is_recruiter)
def edit_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    if request.method == "POST":
        form = NewJobForm(request.POST, instance=job)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect('add-job-detail', slug)
    else:
        form = NewJobForm(instance=job)
    context = {
        'form': form,
        'rec_navbar': 1,
        'job': job,
    }
    return render(request, 'recruiters/edit_job.html', context)

@login_required
@user_passes_test(is_recruiter)
def selected_list(request):
    objects = Selected.objects.select_related('job', 'applicant')
    
    profiles = []
    for obj in objects:
        job = obj.job       
        selected_applicants = objects.filter(job=job).order_by('date_posted')
        for applicant in selected_applicants:
            profile = Profile.objects.filter(user=applicant.id).first()
            if profile is not None:
                profiles.append(profile)
    
    context = {
        'rec_navbar': 1,
        'profiles': profiles,
        'job': job,
    }
    
    return render(request, 'recruiter/selected_list.html', context)

@login_required
@user_passes_test(is_recruiter)
def applicants_list(request):
    
    objects = Applicants.objects.select_related('job', 'applicant')
    profiles = []
    for obj in objects:
        job = obj.job       
        applicants = objects.filter(job=job).order_by('date_posted')
        for applicant in applicants:
            profile = Profile.objects.filter(user=applicant.id).first()
            if profile is not None:
                profiles.append(profile)

    context = {
        'rec_navbar': 1,
        'job':job,
        'applicants':applicants,
        'profiles':profiles
        # 'applicants':applicants
        
    }
    print(context)
    
    return render(request, 'recruiter/applicants_list.html', context)

@login_required
@user_passes_test(is_recruiter)
def select_applicant(request, can_id, job_id):
    job = get_object_or_404(Job, id=job_id)
    profile = get_object_or_404(Profile, user_id=can_id)
    user = profile.user
    
    selected, created = Selected.objects.get_or_create(job=job, applicant=user)
    if created:
        applicant = Applicants.objects.filter(job=job, applicant=user).first()
        if applicant is None:
            messages.error(request, "Applicant {} not select successfully.".format(user.name),
                             extra_tags='alert alert-warning alert-dismissible fade show')
            return redirect('recruiter:applicants_list')
        applicant.delete()
        messages.success(request, "Applicant {} select successfully.".format(user.name),extra_tags='alert alert-success alert-dismissible fade show')
    else:
        messages.warning(request, "Applicant {} already selected.".format(user.name),extra_tags='alert alert-success alert-dismissible fade show')
    
    return redirect('recruiter:applicants_list')


@login_required
@user_passes_test(is_recruiter)
def reject_applicant(request, can_id, job_id):
    job = get_object_or_404(Job, id=job_id)
    profile = get_object_or_404(Profile, user_id=can_id)
    user = profile.user
    
    applicant = Applicants.objects.filter(job=job, applicant=user).first()
    
    if applicant is None:
        messages.error(request, "Applicant {} not reject successfully.".format(user.name),
                            extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect('recruiter:applicants_list')
    applicant.delete()
    messages.success(request, "Applicant {} rejected successfully.".format(user.name),extra_tags='alert alert-success alert-dismissible fade show')

    return redirect('recruiter:applicants_list')

def search_candidate(request):
    
    looking_for = request.GET.get('looking_for') #full time part time
    
    location = request.GET.get('location') 
    
    
    if location or looking_for:
        # Perform the search query using Q objects
        results = Profile.objects.filter(
            Q(looking_for__icontains=looking_for) |
            Q(full_name__icontains=looking_for) |
            Q(grad_year__icontains=looking_for),
            location__icontains=location
        )
        
    else:
        # If both query and location are empty, show all jobs
        results = Profile.objects.all()
        
    paginator = Paginator(results, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'search_candidates_page': "active",
        'rec_navbar': 1,
        'profiles': page_obj,
    }

    return render(request, 'recruiter/search_candidate.html', context)