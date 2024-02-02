from django.urls import path, include


from users.views import *
app_name = 'users'
urlpatterns = [

    path('home/',home, name='home'),
    path('login/',login_view, name='login'),
    path('register/',registration_view, name='register'),
    path('logout/',logout_view, name='logout')
]