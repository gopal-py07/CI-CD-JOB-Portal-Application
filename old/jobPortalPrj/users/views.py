from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth import (
                                  authenticate,
                                  logout ,
                                  login
                              )
from .forms import (
                    
                    UserAuthenticationForm,
                    RegistrationForm
                    
                )

# Create your views here.

def home(request):
    context = {
        
    }
    return render(request, 'home.html', context)


    
def  login_view(request):
    """
      Renders Login Form
    """
    context = {}
    user = request.user
   
    if user.is_authenticated:
        return redirect('users:home')
        # return redirect('users:home')
    if request.POST:
        form    = UserAuthenticationForm(request.POST)
        email   = request.POST.get('email')
        password = request.POST.get('password')
        
        user =  authenticate(email=email, password=password)
        
        if user:
            login(request, user)
            if user.account_type == 'admin':
                return redirect('users:home')
            elif user.account_type == 'candidates':
                return redirect('users:home')
            elif user.account_type == 'recruiter':
                return redirect('users:home')
            messages.success(request, "Logged In",extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('users:home')
            # return redirect('users:home')
        else:
            pass
            # messages.error(,"please Correct Below Errors",)
    else:
        form = UserAuthenticationForm()
    context['login_form'] = form
    
    return render(request, "users/login.html", context)
    
    
def logout_view(request):
    
    logout(request)
    messages.success(request, "Logged Out",  extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('users:home')


def registration_view(request):
    """
      Renders Registration Form 
    """
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST, use_required_attribute=False)
        if form.is_valid():
            form.save()
            email    = form.cleaned_data.get('email')
            messages.success(request, "You have been Registered as {}".format(email), extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('users:login')
        else:
            messages.error(request, "Please Correct Below Errors")
            context['registration_form'] = form
    else:
        form = RegistrationForm(use_required_attribute=False)
        context['registration_form'] = form
    return render(request, "users/register.html", context)








