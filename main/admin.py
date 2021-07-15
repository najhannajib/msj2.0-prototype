from django.contrib import admin
from .models import post, vaccine, health, location_qr, geolocation

# Register your models here.

admin.site.register(post)
admin.site.register(vaccine)
admin.site.register(health)
admin.site.register(location_qr)
admin.site.register(geolocation)

