from django.contrib import admin
from bonus.models import Country, Department, Discover, Disease, Diseasetype, Doctor, Publicservant, Record, Specialize, Users

# Register your models here.

# from .models import Department

# admin.site.register(Department)

admin.site.register(Country)
admin.site.register(Department)
admin.site.register(Discover)
admin.site.register(Disease)
admin.site.register(Diseasetype)
admin.site.register(Doctor)
admin.site.register(Publicservant)
admin.site.register(Record)
admin.site.register(Specialize)
admin.site.register(Users)

