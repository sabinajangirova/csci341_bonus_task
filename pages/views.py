from django.db import connection
from django.db.models import fields
from django.shortcuts import redirect, render
from django.http import HttpResponse
from bonus.models import Country, Department, Discover, Disease, Diseasetype, Doctor, Publicservant, Record, Specialize, Users
import simplejson
from django.views.decorators.csrf import csrf_exempt
import datetime
from bonus.forms import DeathRateForm, DiscoverForm, DiscoverUpdateForm, DiseaseForm, DiseasePublicServantForm, DiseaseTypeForm, DiseaseTypeUpdateForm, DiseaseUpdateForm, DoctorForm, DoctorNumberRankForm, DoctorUpdateForm, MoreDiseaseTypeForm, PathogenDateForm, PublicServantForm, PublicServantUpdateForm, RecordForm, RecordUpdateForm, RecordsRangeForm, SpecializeForm, UsersForm, UsersUpdateForm, CountryForm, CountryUpdateForm, DepartmentForm
# Create your views here.

def home(request):
    return render(request, 'home.html', {})

def statistics(request):
    death_rate_form = DeathRateForm()
    patients_rate_form = DeathRateForm()
    doctor_number_form = DoctorNumberRankForm()
    pathogen_date_form = PathogenDateForm()
    not_specialized_form = DoctorNumberRankForm()
    more_disease_types_form = MoreDiseaseTypeForm()
    salary_specialize_form = DoctorNumberRankForm()
    disease_public_servant_form = DiseasePublicServantForm()
    records_range_form = RecordsRangeForm()
    return render(request, 'statistics.html', {'death_rate_form':death_rate_form, 'patients_rate_form':patients_rate_form, 'doctor_number_form':doctor_number_form, 'pathogen_date_form':pathogen_date_form, 'not_specialized_form':not_specialized_form, 'more_disease_types_form':more_disease_types_form, 'salary_specialize_form':salary_specialize_form, 'disease_public_servant_form':disease_public_servant_form, 'records_range_form':records_range_form})

def country_table(request):
    form = CountryForm()
    return render(request, "country_table.html", {'form':form})

def department_table(request):
    form = DepartmentForm()
    return render(request, "department_table.html", {'form':form})

def discover_table(request):
    form = DiscoverForm()
    return render(request, "discover_table.html", {'form':form})

def disease_table(request):
    form = DiseaseForm()
    return render(request, "disease_table.html", {'form':form})

def disease_type_table(request):
    form = DiseaseTypeForm()
    return render(request, "disease_type.html", {'form':form})

def doctor_table(request):
    form = DoctorForm()
    return render(request, "doctor_table.html", {'form':form})

def public_servant_table(request):
    form = PublicServantForm()
    return render(request, "public_servant_table.html", {'form':form})

def record_table(request):
    form = RecordForm()
    return render(request, "record_table.html", {'form':form})

def specialize_table(request):
    form = SpecializeForm()
    return render(request, "specialize_table.html", {'form':form})

def users_table(request):
    form = UsersForm()

    return render(request, "users_table.html", {'form':form})

def query1(request):
    with connection.cursor() as cursor:
        # List the disease code and the description of diseases that are caused by “bacteria” (pathogen) and were discovered before 1990
        q = 'SELECT "Disease"."disease code", description FROM "Disease" INNER JOIN "Discover" ON "Disease"."disease code" = "Discover"."disease code" WHERE "Disease".pathogen = {pathogen} AND "Discover"."first enc date" < {date}'.format(pathogen = "'bacteria'", date = "'1990-1-1'")
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor)),
        content_type = 'application/javascript; charset=utf8'
    )

def query2(request):
    with connection.cursor() as cursor:
        # List the name, surname and degree of doctors who are not specialized in “infectious diseases
        q = 'SELECT "Users".name, "Users".surname, "Doctor".degree FROM "Users" INNER JOIN "Doctor" ON "Users".email = "Doctor".email INNER JOIN "Specialize" ON "Specialize".email = "Doctor".email INNER JOIN "DiseaseType" ON "Specialize".id = "DiseaseType".id WHERE "Specialize".email NOT IN (SELECT "Specialize".email FROM "Specialize" INNER JOIN "DiseaseType" ON "DiseaseType".id = "Specialize".id WHERE "DiseaseType".description = {description}) GROUP BY "Specialize".email, "Users".name, "Users".surname, "Doctor".degree'.format(description = "'infectious diseases'")
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor)),
        content_type = 'application/javascript; charset=utf8'
    )

def query3(request):
    with connection.cursor() as cursor:
        # List the name, surname and degree of doctors who are specialized in more than 2 disease types
        q = 'SELECT "Users".name, "Users".surname, "Doctor".degree FROM "Doctor" INNER JOIN "Users" ON "Doctor".email = "Users".email INNER JOIN "Specialize" ON "Users".email = "Specialize".email GROUP BY "Doctor".email, "Specialize".email, "Users".email HAVING COUNT("Specialize".id) > 2'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor)),
        content_type = 'application/javascript; charset=utf8'
    )

def query4(request):
    with connection.cursor() as cursor:
        # For each country list the cname and average salary of doctors who are specialized in "virology"
        q = 'SELECT "Country".cname, average FROM "Country" LEFT JOIN (SELECT "Users".cname country_name, AVG("Users".salary) average FROM "Users" LEFT JOIN "Specialize" ON "Users".email = "Specialize".email LEFT JOIN "DiseaseType" ON "Specialize".id = "DiseaseType".id WHERE "DiseaseType".description = {description} GROUP BY "Users".cname) s ON "Country".cname = s.country_name'.format(description = "'virology'")
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True),
        content_type = 'application/javascript; charset=utf8'
    )

def query5(request):
    with connection.cursor() as cursor:
        # List the departments of public servants who report “covid-19” cases in more than one country and the number of such public servants who work in these departments'
        q = 'SELECT "PublicServant".department, COUNT("PublicServant".email) FROM "PublicServant" INNER JOIN (SELECT "PublicServant".department department FROM "PublicServant" INNER JOIN (SELECT "Record".email email FROM "Record" INNER JOIN "Disease" ON "Record"."disease code" = "Disease"."disease code" WHERE "Disease".description = {description} GROUP BY "Record".email HAVING COUNT("Record".cname) > 1) as s ON "PublicServant".email = s.email) p ON "PublicServant".department = p.department GROUP BY "PublicServant".department'.format(description = "'covid-19'")
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True),
        content_type = 'application/javascript; charset=utf8'
    )
@csrf_exempt
def query6(request):
    with connection.cursor() as cursor:
        # 'Double the salary of public servants who have recorded covid-19 patients more than 3 times'
        q = 'UPDATE "Users" SET salary = salary*2  WHERE "Users".email = (SELECT "Users".email FROM "Record" INNER JOIN "Users" ON "Record".email = "Users".email INNER JOIN "Disease" ON "Record"."disease code" = "Disease"."disease code" WHERE "Disease".description = {description} GROUP BY "Record".email, "Users".email HAVING COUNT("Record".cname) > 3)'.format(description = "'covid-19'")
        cursor.execute(q)
        return HttpResponse('Successfully updated the salary')

@csrf_exempt
def query7(request):
    with connection.cursor() as cursor:
        # Delete the users whose surname contain the substring “bek”
        q = 'DELETE FROM "Users" WHERE surname LIKE {substring1} OR surname LIKE {substring2}'.format(substring1 = "'%bek%'", substring2 = "'%Bek%'")
        cursor.execute(q)
        return HttpResponse('Successfully deleted users')
@csrf_exempt
def query8(request):
    with connection.cursor() as cursor:
        # Create index on pathogen
        q = 'CREATE UNIQUE INDEX "idx pathogen" ON "Disease" (pathogen)'
        try:
            cursor.execute(q)
            return HttpResponse('Successfully created index on pathogen')
        except:
            return HttpResponse('The index already exists')

def query9(request):
    with connection.cursor() as cursor:
        # List the email, name, and department of public servants who have created records where the number of patients is between 100000 and 999999
        q = 'SELECT DISTINCT "Users".email, "Users".name, "PublicServant".department FROM "Users" INNER JOIN "PublicServant" ON "Users".email = "PublicServant".email INNER JOIN "Record" ON "Record".email = "PublicServant".email WHERE "Record"."total patients" > 100000 AND "Record"."total patients" < 999999'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True),
        content_type = 'application/javascript; charset=utf8'
    )  

def query10(request):
    with connection.cursor() as cursor:
        # List the top 5 counties with the highest number of total patients recorded
        q = 'SELECT "Record".cname FROM "Record" GROUP BY "Record".cname ORDER by SUM("Record"."total patients") DESC LIMIT 5'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True),
        content_type = 'application/javascript; charset=utf8'
    )

def query11(request):
    with connection.cursor() as cursor:
        # Group the diseases by disease type and the total number of patients treated
        q = 'SELECT "Disease".*, s.treated_patients FROM "Disease" INNER JOIN "DiseaseType" ON "Disease".id = "DiseaseType".id LEFT JOIN (SELECT "Record"."disease code" disease_code, SUM("Record"."total patients") as treated_patients FROM "Record" GROUP BY "Record"."disease code") as s ON s.disease_code = "Disease"."disease code" GROUP BY "DiseaseType".id, s.treated_patients, "Disease"."disease code", "Disease"."pathogen", "Disease"."description"'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True),
        content_type = 'application/javascript; charset=utf8'
    )

def get_countries(request):
    with connection.cursor() as cursor:
        q = 'SELECT * FROM "Country"'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True),
        content_type = 'application/javascript; charset=utf8'
        )

def get_department(request):
    with connection.cursor() as cursor:
        q = 'SELECT * FROM "Department"'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True),
        content_type = 'application/javascript; charset=utf8'
        )

def get_discover(request):
    with connection.cursor() as cursor:
        q = 'SELECT * FROM "Discover"'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True, default = date_converter),
        content_type = 'application/javascript; charset=utf8'
        )

def get_disease(request):
    with connection.cursor() as cursor:
        q = 'SELECT * FROM "Disease"'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True, default = date_converter),
        content_type = 'application/javascript; charset=utf8'
        )

def get_disease_type(request):
    with connection.cursor() as cursor:
        q = 'SELECT * FROM "DiseaseType"'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True, default = date_converter),
        content_type = 'application/javascript; charset=utf8'
        )

def get_doctor(request):
    with connection.cursor() as cursor:
        q = 'SELECT * FROM "Doctor"'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True, default = date_converter),
        content_type = 'application/javascript; charset=utf8'
        )

def get_public_servant(request):
    with connection.cursor() as cursor:
        q = 'SELECT * FROM "PublicServant"'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True, default = date_converter),
        content_type = 'application/javascript; charset=utf8'
        )

def get_record(request):
    with connection.cursor() as cursor:
        q = 'SELECT * FROM "Record"'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True, default = date_converter),
        content_type = 'application/javascript; charset=utf8'
        )

def get_specialize(request):
    with connection.cursor() as cursor:
        q = 'SELECT * FROM "Specialize"'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True, default = date_converter),
        content_type = 'application/javascript; charset=utf8'
        )

def get_users(request):
    with connection.cursor() as cursor:
        q = 'SELECT * FROM "Users"'
        cursor.execute(q)
        return HttpResponse(
        simplejson.dumps(dictfetchall(cursor), use_decimal = True, default = date_converter),
        content_type = 'application/javascript; charset=utf8'
        )

def date_converter(o):
    if isinstance(o, datetime.date):
        return o.__str__()

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@csrf_exempt
def create_user(request):
    usersForm = UsersForm(request.POST)

    if usersForm.is_valid():
        old_user = Users.objects.filter(email = usersForm.cleaned_data['email']).first()
        if old_user is not None:
            return HttpResponse('Such user already exists '+ old_user.email)
        else:
            new_user = Users(email=usersForm.cleaned_data['email'],name=usersForm.cleaned_data['name'], surname=usersForm.cleaned_data['surname'],salary=usersForm.cleaned_data['salary'],phone=usersForm.cleaned_data['phone'],cname=usersForm.cleaned_data['cname'])
            new_user.save()

    return redirect('/user')

@csrf_exempt
def delete_user(request, email):
    user = Users.objects.get(email=email)
    user.delete()

    return redirect('/user')

@csrf_exempt
def edit_user(request, email):
    user = Users.objects.get(email=email)
    updateform = UsersUpdateForm(request.POST)

    if updateform.is_valid():
        updated_user = Users(email=email, name=updateform.cleaned_data['name'], surname=updateform.cleaned_data['surname'],salary=updateform.cleaned_data['salary'],phone=updateform.cleaned_data['phone'],cname=updateform.cleaned_data['cname'])
        updated_user.save()

    return render(request, 'user_edit.html', {'user':user, 'form':updateform})

@csrf_exempt
def create_country(request):
    countryForm = CountryForm(request.POST)

    if countryForm.is_valid():
        old_country = Country.objects.filter(cname = countryForm.cleaned_data['cname']).first()
        if old_country is not None:
            return HttpResponse('Such country already exists '+ old_country.cname)
        else:
            new_country = Country(cname=countryForm.cleaned_data['cname'],population=countryForm.cleaned_data['population'])
            new_country.save()

    return redirect('/country')

@csrf_exempt
def delete_country(request, cname):
    country = Country.objects.get(cname=cname)
    country.delete()

    return redirect('/country')

@csrf_exempt
def edit_country(request, cname):
    country = Country.objects.get(cname=cname)
    updateform = CountryUpdateForm(request.POST)

    if updateform.is_valid():
        updated_country = Country(cname=cname, population=updateform.cleaned_data['population'])
        updated_country.save()

    return render(request, 'country_edit.html', {'country':country, 'form':updateform})

@csrf_exempt
def create_department(request):
    departmentForm = DepartmentForm(request.POST)

    if departmentForm.is_valid():
        old_department = Department.objects.filter(dname=departmentForm.cleaned_data['dname']).first()
        if old_department is not None:
            return HttpResponse('Such department already exists '+ old_department.dname)
        else:
            new_department = Department(dname=departmentForm.cleaned_data['dname'])
            new_department.save()

    return redirect('/department')

@csrf_exempt
def delete_department(request, dname):
    department = Department.objects.get(dname=dname)
    department.delete()

    return redirect('/department')

@csrf_exempt
def create_discover(request):
    discoverForm = DiscoverForm(request.POST)

    if discoverForm.is_valid():
        old_discover = Discover.objects.filter(cname = discoverForm.cleaned_data['cname']).filter(disease_code=discoverForm.cleaned_data['disease_code']).first()
        if old_discover is not None:
            return HttpResponse('Such discover already exists '+ old_discover.cname.cname + " " + old_discover.disease_code.disease_code)
        else:
            if discoverForm.cleaned_data['first_enc_date'] <= datetime.date().today().strftime('%Y-%m-%d'):
                with connection.cursor() as cursor:
                    q = '''INSERT INTO "Discover"(cname, "disease code", "first enc date") VALUES ('{cname}', '{disease_code}', '{first_enc_date}')'''.format(cname = discoverForm.cleaned_data['cname'].cname, disease_code=discoverForm.cleaned_data['disease_code'].disease_code, first_enc_date=discoverForm.cleaned_data['first_enc_date'])
                    cursor.execute(q)
            else:
                return HttpResponse('''The date should be less than today's or equal to it''')
            return redirect('/discover')

@csrf_exempt
def delete_discover(request, cname, disease_code):
    with connection.cursor() as cursor:
        q = '''DELETE FROM "Discover" WHERE cname = '{cname}' AND "disease code" = '{disease_code}' '''.format(cname = cname, disease_code = disease_code)
        cursor.execute(q)

    return redirect('/discover')

@csrf_exempt
def edit_discover(request, cname, disease_code):
    discover = Discover.objects.get(cname=cname, disease_code=disease_code)
    updateform = DiscoverUpdateForm(request.POST)

    if updateform.is_valid():
        if updateform.cleaned_data['first_enc_date'] <= datetime.date().today().strftime('%Y-%m-%d'):
            Discover.objects.filter(cname=cname, disease_code=disease_code).update(first_enc_date = updateform.cleaned_data['first_enc_date'])
        else:
            return HttpResponse('''The date should be less than today's or equal to it''')
    return render(request, 'discover_edit.html', {'discover':discover, 'form':updateform})

@csrf_exempt
def create_disease(request):
    diseaseForm = DiseaseForm(request.POST)

    if diseaseForm.is_valid():
        old_disease = Disease.objects.filter(disease_code=diseaseForm.cleaned_data['disease_code']).first()
        if old_disease is not None:
            return HttpResponse('Such disease already exists '+ old_disease.disease_code)
        else:
            disease = Disease(disease_code = diseaseForm.cleaned_data['disease_code'], pathogen = diseaseForm.cleaned_data['pathogen'], description = diseaseForm.cleaned_data['description'], id = diseaseForm.cleaned_data['id'])
            disease.save()
            return redirect('/disease')

@csrf_exempt
def delete_disease(request, disease_code):
    disease = Disease.objects.get(disease_code=disease_code)
    disease.delete()

    return redirect('/disease')

@csrf_exempt
def edit_disease(request, disease_code):
    disease = Disease.objects.get(disease_code=disease_code)
    updateform = DiseaseUpdateForm(request.POST)

    if updateform.is_valid():
        updated_disease = Disease(disease_code=disease_code, pathogen = updateform.cleaned_data['pathogen'], description = updateform.cleaned_data['description'], id = updateform.cleaned_data['id'])
        updated_disease.save()
        
    return render(request, 'disease_edit.html', {'disease':disease, 'form':updateform})

@csrf_exempt
def create_disease_type(request):
    diseaseTypeForm = DiseaseTypeForm(request.POST)

    if diseaseTypeForm.is_valid():
        old_disease_type = Diseasetype.objects.filter(id=diseaseTypeForm.cleaned_data['id']).first()
        if old_disease_type is not None:
            return HttpResponse('Such disease type already exists '+ old_disease_type.id)
        else:
            diseasetype = Diseasetype(id = diseaseTypeForm.cleaned_data['id'], description = diseaseTypeForm.cleaned_data['description'])
            diseasetype.save()
            return redirect('/disease_type')

@csrf_exempt
def delete_disease_type(request, id):
    diseasetype = Diseasetype.objects.get(id = id)
    diseasetype.delete()

    return redirect('/disease_type')

@csrf_exempt
def edit_disease_type(request, id):
    diseasetype = Diseasetype.objects.get(id = id)
    updateform = DiseaseTypeUpdateForm(request.POST)

    if updateform.is_valid():
        updated_disease_type = Diseasetype(id = id, description = updateform.cleaned_data['description'])
        updated_disease_type.save()

    return render(request, 'disease_type_edit.html', {'disease_type':diseasetype, 'form':updateform})

@csrf_exempt
def create_doctor(request):
    doctorForm = DoctorForm(request.POST)

    if doctorForm.is_valid():
        old_doctor = Doctor.objects.filter(email=doctorForm.cleaned_data['email']).first()
        if old_doctor is not None:
            return HttpResponse('Such doctor already exists '+ old_doctor.email.email)
        else:
            doctor = Doctor(email = doctorForm.cleaned_data['email'], degree = doctorForm.cleaned_data['degree'])
            doctor.save()
            return redirect('/doctor')

@csrf_exempt
def delete_doctor(request, email):
    doctor = Doctor.objects.get(email = email)
    doctor.delete()

    return redirect('/doctor')

@csrf_exempt
def edit_doctor(request, email):
    doctor = Doctor.objects.get(email = email)
    updateform = DoctorUpdateForm(request.POST)

    if updateform.is_valid():
        Doctor.objects.filter(email=email).update(degree = updateform.cleaned_data['degree'])

    return render(request, 'doctor_edit.html', {'doctor':doctor, 'form':updateform})

@csrf_exempt
def create_public_servant(request):
    publicServantForm = PublicServantForm(request.POST)

    if publicServantForm.is_valid():
        old_public_servant = Publicservant.objects.filter(email=publicServantForm.cleaned_data['email']).first()
        if old_public_servant is not None:
            return HttpResponse('Such public servant already exists '+ old_public_servant.email.email)
        else:
            public_servant = Publicservant(email = publicServantForm.cleaned_data['email'], department = publicServantForm.cleaned_data['department'])
            public_servant.save()
            return redirect('/public_servant')

@csrf_exempt
def delete_public_servant(request, email):
    public_servant = Publicservant.objects.get(email = email)
    public_servant.delete()

    return redirect('/public_servant')

@csrf_exempt
def edit_public_servant(request, email):
    public_servant = Publicservant.objects.get(email = email)
    updateform = PublicServantUpdateForm(request.POST)

    if updateform.is_valid():
        Publicservant.objects.filter(email=email).update(department = updateform.cleaned_data['department'])

    return render(request, 'public_servant_edit.html', {'public_servant':public_servant, 'form':updateform})

@csrf_exempt
def create_record(request):
    recordForm = RecordForm(request.POST)

    if recordForm.is_valid():
        old_record = Record.objects.filter(email = recordForm.cleaned_data['email']).filter(cname = recordForm.cleaned_data['cname']).filter(disease_code=recordForm.cleaned_data['disease_code']).first()
        if old_record is not None:
            return HttpResponse('Such record already exists ' + old_record.email.email.email + " " + old_record.cname.cname + " " + old_record.disease_code.disease_code)
        else:
            with connection.cursor() as cursor:
                q = '''INSERT INTO "Record"(email, cname, "disease code", "total deaths", "total patients") VALUES ('{email}', '{cname}', '{disease_code}', '{total_deaths}', '{total_patients}')'''.format(email = recordForm.cleaned_data['email'].email.email,  cname = recordForm.cleaned_data['cname'].cname, disease_code=recordForm.cleaned_data['disease_code'].disease_code, total_deaths=recordForm.cleaned_data['total_deaths'], total_patients=recordForm.cleaned_data['total_patients'])
                cursor.execute(q)
            return redirect('/record')

@csrf_exempt
def delete_record(request, email, cname, disease_code):
    with connection.cursor() as cursor:
        q = '''DELETE FROM "Record" WHERE email = '{email}' AND cname = '{cname}' AND "disease code" = '{disease_code}' '''.format(email=email, cname = cname, disease_code = disease_code)
        cursor.execute(q)

    return redirect('/record')

@csrf_exempt
def edit_record(request, email, cname, disease_code):
    record = Record.objects.get(email=email,cname=cname, disease_code=disease_code)
    updateform = RecordUpdateForm(request.POST)

    if updateform.is_valid():
        Record.objects.filter(cname=cname, disease_code=disease_code).update(total_deaths = updateform.cleaned_data['total_deaths'], total_patients=updateform.cleaned_data['total_patients'])

    return render(request, 'record_edit.html', {'record':record, 'form':updateform})

@csrf_exempt
def create_specialize(request):
    specializeForm = SpecializeForm(request.POST)

    if specializeForm.is_valid():
        old_specialize = Specialize.objects.filter(id = specializeForm.cleaned_data['id']).filter(email = specializeForm.cleaned_data['email']).first()
        if old_specialize is not None:
            return HttpResponse('Such specialize already exists ' + str(old_specialize.id.id) + " " + old_specialize.email.email.email)
        else:
            with connection.cursor() as cursor:
                q = '''INSERT INTO "Specialize"(id, email) VALUES ('{id}', '{email}')'''.format(id = specializeForm.cleaned_data['id'].id,  email = specializeForm.cleaned_data['email'].email.email)
                cursor.execute(q)
            return redirect('/specialize')

@csrf_exempt
def delete_specialize(request, id, email):
    with connection.cursor() as cursor:
        q = '''DELETE FROM "Specialize" WHERE id = '{id}' AND email = '{email}' '''.format(id=id, email=email)
        cursor.execute(q)

    return redirect('/specialize')

def death_rate(request):
    death_rate_form = DeathRateForm(request.POST)
    if death_rate_form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute('''SELECT cname, 100.0*SUM("total deaths")/SUM("total patients") as percent FROM "Record" WHERE "disease code" = '{disease_code}' GROUP BY cname ORDER BY percent DESC'''.format(disease_code = death_rate_form.cleaned_data['disease_code'].disease_code))
            return render(request, "statistics.html", {'rank_death_rate':cursor, 'death_rate_form':death_rate_form})

def patients_rate(request):
    patients_rate_form = DeathRateForm(request.POST)
    if patients_rate_form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute('''SELECT "Country".cname, 100.0*subquery.sum_p/population as percent FROM "Country" INNER JOIN (SELECT cname, SUM("total patients") as sum_p FROM "Record" WHERE "disease code" = '{disease_code}' GROUP BY cname) as subquery ON "Country".cname = subquery.cname ORDER BY percent DESC '''.format(disease_code = patients_rate_form.cleaned_data['disease_code'].disease_code))
            return render(request, "statistics.html", {'patients_rate':cursor, 'patients_rate_form':patients_rate_form})

def doctor_number(request):
    doctor_number_form = DoctorNumberRankForm(request.POST)
    if doctor_number_form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute('''SELECT "Users".cname, COUNT("Users".email) as d_number FROM "Users" INNER JOIN "Specialize" ON "Users".email = "Specialize".email WHERE "Specialize".id = {id} GROUP BY "Users".cname ORDER BY d_number DESC '''.format(id = doctor_number_form.cleaned_data['id'].id))
            return render(request, "statistics.html", {'doctor_number':cursor, 'doctor_number_form':doctor_number_form})

def average_salary(request):
    with connection.cursor() as cursor:
            cursor.execute('''SELECT "Users".cname, AVG("Users".salary) as avg_salary FROM "Users" GROUP BY "Users".cname ''')
            return render(request, "statistics.html", {'average_salary':cursor})

def pathogen_date(request):
    pathogen_date_form = PathogenDateForm(request.POST)

    if pathogen_date_form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute('''SELECT "Disease"."disease code", description FROM "Disease" INNER JOIN "Discover" ON "Disease"."disease code" = "Discover"."disease code" WHERE "Disease".pathogen = '{pathogen}' AND "Discover"."first enc date" < '{date}' '''.format(pathogen = pathogen_date_form.cleaned_data['pathogen'], date = pathogen_date_form.cleaned_data['date']))
            return render(request, "statistics.html", {'pathogen_date':dictfetchall(cursor), 'pathogen_date_form':pathogen_date_form})

def not_specialized(request):
    not_specialized_form = DoctorNumberRankForm(request.POST)

    if not_specialized_form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute('''SELECT "Users".name, "Users".surname, "Doctor".degree FROM "Users" INNER JOIN "Doctor" ON "Users".email = "Doctor".email INNER JOIN "Specialize" ON "Specialize".email = "Doctor".email INNER JOIN "DiseaseType" ON "Specialize".id = "DiseaseType".id WHERE "Specialize".email NOT IN (SELECT "Specialize".email FROM "Specialize" INNER JOIN "DiseaseType" ON "DiseaseType".id = "Specialize".id WHERE "DiseaseType".id = {id}) GROUP BY "Specialize".email, "Users".name, "Users".surname, "Doctor".degree '''.format(id = not_specialized_form.cleaned_data['id'].id))
            return render(request, "statistics.html", {'not_specialized':dictfetchall(cursor), 'not_specialized_form':not_specialized_form})

def more_disease_types(request):
    more_disease_types_form = MoreDiseaseTypeForm(request.POST)

    if more_disease_types_form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute('''SELECT "Users".name, "Users".surname, "Doctor".degree FROM "Doctor" INNER JOIN "Users" ON "Doctor".email = "Users".email INNER JOIN "Specialize" ON "Users".email = "Specialize".email GROUP BY "Doctor".email, "Specialize".email, "Users".email HAVING COUNT("Specialize".id) > '{number}' '''.format(number = more_disease_types_form.cleaned_data['number']))
            return render(request, "statistics.html", {'more_disease_types':dictfetchall(cursor), 'more_disease_types_form':more_disease_types_form})

def salary_specialize(request):
    salary_specialize_form = DoctorNumberRankForm(request.POST)

    if salary_specialize_form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute('''SELECT "Country".cname, average FROM "Country" LEFT JOIN (SELECT "Users".cname country_name, AVG("Users".salary) average FROM "Users" LEFT JOIN "Specialize" ON "Users".email = "Specialize".email LEFT JOIN "DiseaseType" ON "Specialize".id = "DiseaseType".id WHERE "DiseaseType".id = {id} GROUP BY "Users".cname) s ON "Country".cname = s.country_name '''.format(id = salary_specialize_form.cleaned_data['id'].id))
            return render(request, "statistics.html", {'salary_specialize':dictfetchall(cursor), 'salary_specialize_form':salary_specialize_form})

def disease_public_servant(request):
    disease_public_servant_form = DiseasePublicServantForm(request.POST)

    if disease_public_servant_form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute('''SELECT "PublicServant".department, COUNT("PublicServant".email) FROM "PublicServant" INNER JOIN (SELECT "PublicServant".department department FROM "PublicServant" INNER JOIN (SELECT "Record".email email FROM "Record" INNER JOIN "Disease" ON "Record"."disease code" = "Disease"."disease code" WHERE "Disease"."disease code" = '{disease_code}' GROUP BY "Record".email HAVING COUNT("Record".cname) > 1) as s ON "PublicServant".email = s.email) p ON "PublicServant".department = p.department GROUP BY "PublicServant".department '''.format(disease_code = disease_public_servant_form.cleaned_data['disease_code'].disease_code))
            return render(request, "statistics.html", {'disease_public_servant':dictfetchall(cursor), 'disease_public_servant_form':disease_public_servant_form})

def records_range(request):
    records_range_form = RecordsRangeForm(request.POST)

    if records_range_form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute('''SELECT DISTINCT "Users".email, "Users".name, "PublicServant".department FROM "Users" INNER JOIN "PublicServant" ON "Users".email = "PublicServant".email INNER JOIN "Record" ON "Record".email = "PublicServant".email WHERE "Record"."total patients" > {less} AND "Record"."total patients" < {more} '''.format(less = records_range_form.cleaned_data['less'], more = records_range_form.cleaned_data['more']))
            return render(request, "statistics.html", {'records_range':dictfetchall(cursor), 'records_range_form':records_range_form})

def group_by_disease_type(request):
    with connection.cursor() as cursor:
            cursor.execute('''SELECT "Record".cname, "DiseaseType".description, COUNT("DiseaseType".description) FROM "Record" INNER JOIN "Disease" ON "Record"."disease code" = "Disease"."disease code" INNER JOIN "DiseaseType" ON "DiseaseType".id = "Disease".id GROUP BY "Record".cname, "DiseaseType".id  ''')
            return render(request, "statistics.html", {'group_by_disease_type':cursor})

def rank_pathogens(request):
    with connection.cursor() as cursor:
        cursor.execute(''' SELECT "Disease".pathogen, 100.0*SUM("total deaths")/SUM("total patients") as percent FROM "Disease" INNER JOIN "Record" ON "Disease"."disease code" = "Record"."disease code" GROUP BY "Disease".pathogen ORDER BY percent DESC  ''')
        return render(request, "statistics.html", {'rank_pathogens':cursor})