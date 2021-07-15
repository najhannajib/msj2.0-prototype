
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

# Create your views here.


def register(request):
    if(request.method == 'POST'):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Account Created')
            return redirect('login')

    else:
        form = RegisterForm()
    return render(request, 'user/register.html',{'form':form})

@login_required
def profile(request):
    return render(request,'user/profile.html')


def profileupdate(request):
    
    if (request.method == 'POST'):
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if pform.is_valid:
            pform.save()
            return redirect('profile')
    else:
        pform = ProfileUpdateForm(instance=request.user.profile)

    return render(request,'user/profileupdate.html', {'pform':pform})