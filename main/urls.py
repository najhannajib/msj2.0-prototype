from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # path('', TweetListView.as_view(), name='home'),
    path('', views.home, name='home'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/del/', views.PostDeleteView.as_view(), name='post-delete'),

    path('health/', views.health, name='health'),
    path('healthupdate/', views.healthupdate, name='healthupdate'),

    path('vaccine/', views.vaccineview, name= 'vaccine'),
    path('vaccineregister/', views.vaccine, name='vaccineregister'),


    path('qrcode/', views.qrcode, name='qrcode'),
    path('qrcreate/', views.create_qr, name='qrcreate'),
    # path('qrupdate/<int:pk>/', views.update_qr , name='qr-update'),


    path('location/', views.location, name='location'),
    path('locationsubmit/', views.submit_loc, name='locationsubmit')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)