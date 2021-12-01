# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MinValueValidator


class Country(models.Model):
    cname = models.CharField(primary_key=True, max_length=50)
    population = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        managed = False
        db_table = 'Country'


class Department(models.Model):
    dname = models.CharField(primary_key=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'Department'


class Discover(models.Model):
    cname = models.OneToOneField(Country, models.DO_NOTHING, db_column='cname', primary_key=True)
    disease_code = models.ForeignKey('Disease', models.DO_NOTHING, db_column='disease code')  # Field renamed to remove unsuitable characters.
    first_enc_date = models.DateField(db_column='first enc date')  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Discover'
        unique_together = (('cname', 'disease_code'),)


class Disease(models.Model):
    disease_code = models.CharField(db_column='disease code', primary_key=True, max_length=50)  # Field renamed to remove unsuitable characters.
    pathogen = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=140)
    id = models.ForeignKey('Diseasetype', models.DO_NOTHING, db_column='id')

    class Meta:
        managed = False
        db_table = 'Disease'


class Diseasetype(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=140)

    class Meta:
        managed = False
        db_table = 'DiseaseType'


class Doctor(models.Model):
    email = models.OneToOneField('Users', models.DO_NOTHING, db_column='email', primary_key=True)
    degree = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'Doctor'


class Publicservant(models.Model):
    email = models.OneToOneField('Users', models.DO_NOTHING, db_column='email', primary_key=True)
    department = models.ForeignKey(Department, models.DO_NOTHING, db_column='department')

    class Meta:
        managed = False
        db_table = 'PublicServant'


class Record(models.Model):
    email = models.OneToOneField(Publicservant, models.DO_NOTHING, db_column='email', primary_key=True)
    cname = models.ForeignKey(Country, models.DO_NOTHING, db_column='cname')
    disease_code = models.ForeignKey(Disease, models.DO_NOTHING, db_column='disease code')  # Field renamed to remove unsuitable characters.
    total_deaths = models.IntegerField(db_column='total deaths', default=0, validators=[MinValueValidator(0)])  # Field renamed to remove unsuitable characters.
    total_patients = models.IntegerField(db_column='total patients', default=0, validators=[MinValueValidator(0)])  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Record'
        unique_together = (('email', 'cname', 'disease_code'),)


class Specialize(models.Model):
    id = models.OneToOneField(Diseasetype, models.DO_NOTHING, db_column='id', primary_key=True)
    email = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='email')

    class Meta:
        managed = False
        db_table = 'Specialize'
        unique_together = (('id', 'email'),)


class Users(models.Model):
    email = models.CharField(primary_key=True, max_length=60)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40)
    salary = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    phone = models.CharField(max_length=20)
    cname = models.ForeignKey(Country, models.DO_NOTHING, db_column='cname')

    class Meta:
        managed = False
        db_table = 'Users'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'