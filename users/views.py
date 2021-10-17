from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import user_logged_in
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateFrom, ProfileUpdateForm
from django.contrib.auth.models import User


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            user = User.objects.filter(username=username).first()
            login(request,user)
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    current_user = request.user
    if request.method == "POST":
        u_form = UserUpdateFrom(request.POST,instance=current_user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=current_user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateFrom(instance=current_user)
        p_form = ProfileUpdateForm(instance=current_user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form,
        'users':current_user
    }
    return render(request,'users/profile.html',context)