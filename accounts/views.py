from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomedUserCreateForm, CustomedUserUpdateForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('sneakers:index')

    if request.method == "POST":
        print(request.POST)
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user()) 
            return redirect(request.GET.get('next') or 'sneakers:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect("sneakers:index")

# render policy page before going on to sign up page
def signup(request):
    return render(request, 'accounts/policy.html')

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'POST': # sign up
        form = CustomedUserCreateForm(request.POST, request.FILES)
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

# delete account
@require_POST
def userDelete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('sneakers:index')

@login_required
@require_http_methods(['GET', 'POST'])
def userUpdate(request):
    if request.method == 'POST': 
        form = CustomedUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('sneakers:index')
    else:
        form = CustomedUserUpdateForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)
    
@login_required
@require_http_methods(['GET', 'POST'])
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        # form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)
