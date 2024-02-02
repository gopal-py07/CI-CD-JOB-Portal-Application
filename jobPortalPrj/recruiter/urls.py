from django.urls import path, include


from recruiter.views import *
app_name = 'recruiter'
urlpatterns = [

    path('rec_detail', get_rec_details, name='rec-detail'),
    path('listJobs/',getJob_list, name='listJobs'),
    path('add_jobs/',add_job, name='add_jobs'),
    path('job/<slug>', job_detail, name='add-job-detail'),
    
    path('job/selected_list/', selected_list, name='selected_list'),
    path('job/applicants_list/', applicants_list, name='applicants_list'),
    
    path('job/<int:job_id>/select_applicant/<int:can_id>/', select_applicant, name='select_applicant'),
    
    path('job/<int:job_id>/reject_applicant/<int:can_id>/', reject_applicant, name='reject_applicant'),
    
    path('search_candidate/', search_candidate, name='search_candidate')

]