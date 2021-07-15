import django
from django.contrib import messages
from django.db.models import fields
from django.http import request
from django.shortcuts import redirect, render
from django.views.generic.edit import DeleteView, UpdateView
from .models import post, location_qr, geolocation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView
from .forms import healthupdateform, vaccineform, qrcreateform
from django.contrib.auth.models import User
import sys
from django.db.models import Count
import requests
import json
from user.models import profile
# Create your views here.

@login_required
def home(request):
    context = {'posts':post.objects.all, 'location': geolocation.objects.filter(author=request.user)}
    return render(request, 'main/home.html', context)


def is_users(post_user, logged_user):
    return post_user == logged_user


PAGINATION_COUNT = 3


# class home(LoginRequiredMixin, ListView):
#     model = post
#     template_name = 'main/home.html'
#     ordering = ['-date_posted']

    
        


class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['text']
    template_name = 'main/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['text']
    template_name = 'main/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Edit a post'
        return data


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    template_name = 'main/post_delete.html'
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)


# vaccine

def vaccineview(request):
    return render(request, 'main/vaccine.html')


def vaccine(request):
    if (request.method == 'POST'):
        vform = vaccineform(
            request.POST, request.FILES, instance=request.user.vaccine)
        if vform.is_valid:
            vform.save()
            return redirect('vaccine')
    else:
        vform = vaccineform(instance=request.user.vaccine)

    return render(request, 'main/vaccine_register.html', {'vform': vform})


# health
# @login_required
def health(request):
    return render(request, 'main/health.html')


def healthupdate(request):
    # hform =  healthupdateform()
    # return render(request,'main/healthupdate .html', {'hform': hform})

    if (request.method == 'POST'):
        hform = healthupdateform(
            request.POST, request.FILES, instance=request.user.health)
        if hform.is_valid:
            hform.save()
            return redirect('health')
    else:
        hform = healthupdateform(instance=request.user.health)

    return render(request, 'main/healthupdate.html', {'hform': hform})


# qrcode

def qrcode(request):
    context = {'qrcode': location_qr.objects.filter(author=request.user)}
    return render(request, 'main/qrcode.html', context)

# class qrcode(LoginRequiredMixin, ListView):
#     model = location_qr
#     print (location_qr.objects.all)
#     template_name = 'main/qrcode.html'
#     # context_object_name = 'posts'
#     paginate_by = PAGINATION_COUNT
    

def create_qr(request):
    print(request.POST)
    print(request.user)

    if (request.method == 'POST'):

        qr = location_qr.objects.create()
        qr.name = request.POST['name']
        qr.address = request.POST['address']
        qr.city = request.POST['city']
        qr.state = request.POST['state']
        qr.author = request.user
        qr.save()
        

        return redirect('qrcode')
    else:
        form = qrcreateform()

    return render(request, 'main/qr_create.html', {'form': form})


# location

locationdata = {}
@login_required
def location(request):

    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/' +
                       ip_data["ip"])  # data from json
    location_data_one = res.text
    # convert jason to python dictionary
    location_data = json.loads(location_data_one)

    locationdata = location_data

    return render(request, 'main/location.html', {'data': location_data})


def submit_loc(request):

    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/' +
                       ip_data["ip"])  # data from json
    location_data_one = res.text
    # convert jason to python dictionary
    location_data = json.loads(location_data_one)

    locationdata = location_data
    
    loc = geolocation.objects.create()
    loc.country = locationdata["country"]
    loc.regionName = locationdata["regionName"]
    loc.city = locationdata["city"]
    loc.zip = locationdata["zip"]
    loc.latitude = locationdata["lat"]
    loc.longitude = locationdata["lon"]
    loc.country_code = locationdata["countryCode"]
    loc.timezone = locationdata["timezone"]
    loc.author = request.user
    loc.save()

    return render(request, 'main/location.html', {'data': location_data})
