from django import forms
from django.forms.models import ModelChoiceField

from .models import Country, Department, Disease, Diseasetype, Doctor, Publicservant, Users

class CountryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.cname

class DiseaseModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.disease_code

class DiseaseTypeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.id

class UsersModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.email

class PublicservantModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.email.email

class DepartmentModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.dname

class DoctorModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.email.email

class DiseaseForDeathRateModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.disease_code + " - " + obj.description

class DiseasetypeForDoctorNumberModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.id) + " - " + obj.description

class UsersForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=40)
    salary = forms.IntegerField()
    phone = forms.CharField(max_length=20)
    cname = CountryModelChoiceField(queryset=Country.objects.all(), to_field_name="cname")

class UsersUpdateForm(forms.Form):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=40)
    salary = forms.IntegerField()
    phone = forms.CharField(max_length=20)
    cname = CountryModelChoiceField(queryset=Country.objects.all(), to_field_name="cname")

class CountryForm(forms.Form):
    cname = forms.CharField(max_length=50)
    population = forms.IntegerField()

class CountryUpdateForm(forms.Form):
    population = forms.IntegerField()

class DepartmentForm(forms.Form):
    dname = forms.CharField(max_length=10)
        
class DiscoverForm(forms.Form):
    cname = CountryModelChoiceField(queryset=Country.objects.all(), to_field_name="cname")
    disease_code = DiseaseModelChoiceField(queryset=Disease.objects.all(), to_field_name="disease_code")
    first_enc_date = forms.DateField()

class DiscoverUpdateForm(forms.Form):
    first_enc_date = forms.DateField()

class DiseaseForm(forms.Form):
    disease_code = forms.CharField(max_length=50)
    pathogen = forms.CharField(max_length=20)
    description = forms.CharField(max_length=140)
    id = DiseaseTypeModelChoiceField(queryset=Diseasetype.objects.all(), to_field_name="id")

class DiseaseUpdateForm(forms.Form):
    pathogen = forms.CharField(max_length=20)
    description = forms.CharField(max_length=140)
    id = DiseaseTypeModelChoiceField(queryset=Diseasetype.objects.all(), to_field_name="id")

class DiseaseTypeForm(forms.Form):
    id = forms.IntegerField()
    description = forms.CharField(max_length=140)

class DiseaseTypeUpdateForm(forms.Form):
    description = forms.CharField(max_length=140)

class DoctorForm(forms.Form):
    email = UsersModelChoiceField(queryset=Users.objects.all(), to_field_name="email")
    degree = forms.CharField(max_length=20)

class DoctorUpdateForm(forms.Form):
    degree = forms.CharField(max_length=20)

class PublicServantForm(forms.Form):
    email = UsersModelChoiceField(queryset=Users.objects.all(), to_field_name="email")
    department = DepartmentModelChoiceField(queryset=Department.objects.all(), to_field_name="dname")

class PublicServantUpdateForm(forms.Form):
    department = DepartmentModelChoiceField(queryset=Department.objects.all(), to_field_name="dname")

class RecordForm(forms.Form):
    email = PublicservantModelChoiceField(queryset=Publicservant.objects.all(), to_field_name="email")
    cname = CountryModelChoiceField(queryset=Country.objects.all(), to_field_name="cname")
    disease_code = DiseaseModelChoiceField(queryset=Disease.objects.all(), to_field_name="disease_code")
    total_deaths = forms.IntegerField()
    total_patients = forms.IntegerField()

class RecordUpdateForm(forms.Form):
    total_deaths = forms.IntegerField()
    total_patients = forms.IntegerField()

class SpecializeForm(forms.Form):
    id = DiseaseTypeModelChoiceField(queryset=Diseasetype.objects.all(), to_field_name="id")
    email = DoctorModelChoiceField(queryset=Doctor.objects.all(), to_field_name='email')

class DeathRateForm(forms.Form):
    disease_code = DiseaseForDeathRateModelChoiceField(queryset=Disease.objects.all(), to_field_name="disease_code")

class DoctorNumberRankForm(forms.Form):
    id = DiseasetypeForDoctorNumberModelChoiceField(queryset=Diseasetype.objects.all(), to_field_name="id")

class PathogenDateForm(forms.Form):
    pathogen = forms.CharField(max_length=20)
    date = forms.DateField()

class MoreDiseaseTypeForm(forms.Form):
    number = forms.IntegerField()

class DiseasePublicServantForm(forms.Form):
    disease_code = DiseaseForDeathRateModelChoiceField(queryset=Disease.objects.all(), to_field_name="disease_code")

class RecordsRangeForm(forms.Form):
    less = forms.IntegerField()
    more = forms.IntegerField()