"""csci341_bonus_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from pages import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('statistics', views.statistics, name = 'statistics'),
    path('country/', views.country_table, name = 'country'),
    path('department/', views.department_table, name = 'department'),
    path('discover/', views.discover_table, name = 'discover'),
    path('disease/', views.disease_table, name = 'disease'),
    path('disease_type/', views.disease_type_table, name = 'disease_type'),
    path('doctor/', views.doctor_table, name = 'doctor'),
    path('public_servant/', views.public_servant_table, name = 'public_servant'),
    path('record/', views.record_table, name = 'record'),
    path('specialize/', views.specialize_table, name = 'specialize'),
    path('user/', views.users_table, name = 'users'),
    path('api/query1', views.query1),
    path('api/query2', views.query2),
    path('api/query3', views.query3),
    path('api/query4', views.query4),
    path('api/query5', views.query5),
    path('api/query6', views.query6),
    path('api/query7', views.query7),
    path('api/query8', views.query8),
    path('api/query9', views.query9),
    path('api/query10', views.query10),
    path('api/query11', views.query11),
    path('country/api/get', views.get_countries),
    path('department/api/get', views.get_department),
    path('discover/api/get', views.get_discover),
    path('disease/api/get', views.get_disease),
    path('disease_type/api/get', views.get_disease_type),
    path('doctor/api/get', views.get_doctor),
    path('public_servant/api/get', views.get_public_servant),
    path('record/api/get', views.get_record),
    path('specialize/api/get', views.get_specialize),
    path('user/api/get', views.get_users),
    path('user/create_user', views.create_user),
    path('user/edit/<str:email>', views.edit_user),
    path('user/delete/<str:email>', views.delete_user),
    path('country/create_country', views.create_country),
    path('country/edit/<str:cname>', views.edit_country),
    path('country/delete/<str:cname>', views.delete_country),
    path('department/create_department', views.create_department),
    path('department/delete/<str:dname>', views.delete_department),
    path('country/delete/<str:cname>', views.delete_country),
    path('department/create_department', views.create_department),
    path('department/delete/<str:dname>', views.delete_department),
    path('discover/create_discover', views.create_discover),
    path('discover/edit/<str:cname>/<str:disease_code>', views.edit_discover),
    path('discover/delete/<str:cname>/<str:disease_code>', views.delete_discover),
    path('disease/create_disease', views.create_disease),
    path('disease/edit/<str:disease_code>', views.edit_disease),
    path('disease/delete/<str:disease_code>', views.delete_disease),
    path('disease_type/create_disease_type', views.create_disease_type),
    path('disease_type/edit/<int:id>', views.edit_disease_type),
    path('disease_type/delete/<int:id>', views.delete_disease_type),
    path('doctor/create_doctor', views.create_doctor),
    path('doctor/edit/<str:email>', views.edit_doctor),
    path('doctor/delete/<str:email>', views.delete_doctor),
    path('public_servant/create_public_servant', views.create_public_servant),
    path('public_servant/edit/<str:email>', views.edit_public_servant),
    path('public_servant/delete/<str:email>', views.delete_public_servant),
    path('record/create_record', views.create_record),
    path('record/edit/<str:email>/<str:cname>/<str:disease_code>', views.edit_record),
    path('record/delete/<str:email>/<str:cname>/<str:disease_code>', views.delete_record),
    path('specialize/create_specialize', views.create_specialize),
    path('specialize/delete/<int:id>/<str:email>', views.delete_specialize),
    path('statistics/death_rate', views.death_rate),
    path('statistics/patients_rate', views.patients_rate),
    path('statistics/doctor_number', views.doctor_number),
    path('statistics/average_salary', views.average_salary),
    path('statistics/pathogen_date', views.pathogen_date),
    path('statistics/not_specialized', views.not_specialized),
    path('statistics/more_disease_types', views.more_disease_types),
    path('statistics/salary_specialize', views.salary_specialize),
    path('statistics/disease_public_servant', views.disease_public_servant),
    path('statistics/records_range', views.records_range),
    path('statistics/group_by_disease_type', views.group_by_disease_type),
    path('statistics/rank_pathogens', views.rank_pathogens),
    path('admin/', admin.site.urls),
]
