from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from recruiter.models import Job,Applicants, Selected
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from .models import Profile, Skill, AppliedJobs, SavedJobs
from .forms import NewSkillForm,  ProfileUpdateForm
from django.contrib import messages
from users.decortor import is_candidate,check_ac_type_candidates_or_recruiter
from django.contrib.auth.decorators import user_passes_test

from django.db.models import Q


# Create your views here.
@login_required
def home(request):
    context={
        
    }
    return render(request, 'home.html', context)


def candidate_details(request):
    return render(request, 'candidates/details.html')


@login_required
@user_passes_test(is_candidate)
def job_search_list(request):
    
    query = request.GET.get('jobs')
    
    location = request.GET.get('location')
   

    if query or location:
        # Perform the search query using Q objects
        results = Job.objects.filter(
            Q(title__icontains=query) |
            Q(skills_req__icontains=query) |
            Q(company__icontains=query) |
            Q(job_type__icontains=query),
            location__icontains=location
        ).order_by('-date_posted')
        
    else:
        # If both query and location are empty, show all jobs
        results = Job.objects.all()
        
    paginator = Paginator(results, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'jobs': page_obj,
        'query': query,
    }
    return render(request, 'candidates/job_search_list.html', context)


def my_profile(request):
    
    user = request.user
    
    profile = Profile.objects.filter(user=user).first()
    
    user_skills = Skill.objects.filter(user=user)
    
    if request.method == 'POST':
        form = NewSkillForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            return redirect('candidates:my-profile')
    else:
        form = NewSkillForm()
    context = {
        'user': user,
        'profile': profile,
        'skills': user_skills,
        'form': form,
        'profile_page': "active",
    }
    return render(request, 'candidates/profile.html', context)


@login_required
@user_passes_test(is_candidate)
def delete_skill(request, pk=None):
    if request.method == 'POST':
        id_list = request.POST.getlist('choices')
        for skill_id in id_list:
            Skill.objects.get(id=skill_id).delete()
        return redirect('candidates:my-profile')
    
    
@login_required
@user_passes_test(is_candidate)    
def edit_profile(request):
    username = request.user
    profile = Profile.objects.filter(user=username).first()
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = username
            data.save()
            return redirect('candidates:my-profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    context = {
        'form': form,
    }
    return render(request, 'candidates/edit_profile.html', context )


@login_required
@user_passes_test(is_candidate)
def apply_job(request, pk):
    
    username = request.user

    job = get_object_or_404(Job, id=pk)
  
    applied, created = AppliedJobs.objects.get_or_create(job=job, user=username)
    
    if created:
    
        applicant, creation = Applicants.objects.get_or_create(job=job, applicant=username)
    
        messages.success(request, "Apply Job {} successfully.".format(job.title),
                             extra_tags='alert alert-success alert-dismissible fade show')
    else:
        messages.warning(request, "Already Apply Job {} .".format(job.title),
                             extra_tags='alert alert-success alert-dismissible fade show')
    
    return redirect("candidates:job_search_list")
    # return HttpResponseRedirect('candidates/job/{}'.format(job.id))
    
@login_required
@user_passes_test(is_candidate)
def job_detail(request,pk):
    
    job = get_object_or_404(Job, id=pk) 
    
    profile = Profile.objects.filter(user=request.user).select_related('user').first()
    
    has_applied = AppliedJobs.objects.filter(user=request.user).filter(job=job).exists()
    
    has_saved = SavedJobs.objects.filter(user=request.user).filter(job=job).exists()
      
    context={
        
        'job':job,
        'profile':profile,
        'has_applied':has_applied,
        'has_saved':has_saved
    }

    return render(request, 'candidates/job_details.html', context)

@login_required
@user_passes_test(is_candidate)
def profile_view(request, pk):
    profile = Profile.objects.filter(user_id=pk).first()
    username = profile.user
    user_skills = Skill.objects.filter(user=username)
    context = {
        'username':username,
        'profile': profile,
        'skills': user_skills,
    }
    return render(request, 'candidates/profile.html', context)

@login_required
@user_passes_test(is_candidate)
def save_job(request, pk):
    user = request.user
    job = get_object_or_404(Job, id=pk)
    saved, created = SavedJobs.objects.get_or_create(job=job, user=user)
    print(created)
    print(saved)
    return redirect('candidates:job_search_list')



@login_required
@user_passes_test(is_candidate)
def saved_jobs(request):
    jobs = SavedJobs.objects.filter(
        user=request.user).order_by('-date_posted')
   
    return render(request, 'candidates/saved_jobs.html', {'jobs': jobs, 'candidate_navbar': 1})


@login_required
def applied_jobs(request):
    jobs = AppliedJobs.objects.filter(
        user=request.user).order_by('-date_posted')
    statuses = []
    for job in jobs:
        if Selected.objects.filter(job=job.job).filter(applicant=request.user).exists():
            statuses.append(0)
        elif Applicants.objects.filter(job=job.job).filter(applicant=request.user).exists():
            statuses.append(1)
        else:
            statuses.append(2)
    zipped = zip(jobs, statuses)
    return render(request, 'candidates/applied_jobs.html', {'zipped': zipped, 'candidate_navbar': 1})



@login_required
def remove_job(request, pk):
    user = request.user
    job = get_object_or_404(Job, id=pk)
    saved_job = SavedJobs.objects.filter(job=job, user=user).first()
    saved_job.delete()
    return redirect('candidates:job_search_list')