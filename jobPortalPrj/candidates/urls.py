from django.urls import path, include


from candidates.views import *
app_name = 'candidates'
urlpatterns = [
    path('home/', home, name='home'),
    path('details/', candidate_details, name='details'),
    path('job_search_list/', job_search_list, name='job_search_list'),
    
   
    path('profile/', my_profile, name='my-profile'),
    path('delete_skills/', delete_skill, name='skill-delete'),
    path('edit_profile/', edit_profile, name='edit-profile'),
    path('profile/<int:pk>', profile_view, name='profile-view'),
    
    path('job_detcails/<int:pk>/', job_detail, name='job_details'),
    
    path('job/<int:pk>/save/', save_job, name='save-job'),
    path('saved_job_list/', saved_jobs, name='saved-jobs'),

    path('job/<int:pk>/apply/', apply_job, name='apply_job'),
    path('applied_job_list/', applied_jobs, name='applied-jobs'),
    
    path('job/<int:pk>/remove/', remove_job, name='remove-job'),
]
     