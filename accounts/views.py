from django.shortcuts import render, redirect
from .forms import CustomedUserCreateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.

def login(request):

    if request.user.is_authenticated:
        print('request.user.is_authenticated:')
        return redirect('sneakers:index')

    if request.method == "POST":
        print(request.POST)
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user()) 
            return redirect('sneakers:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect("sneakers:index")

# render policy page before going on to sign up page
def signup(request):
    return render(request, 'accounts/policy.html')

def register(request):
    if request.method == 'POST': # sign up
        form = CustomedUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else: # sign up page rendering
        form = CustomedUserCreateForm() # empty form
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html',context)
