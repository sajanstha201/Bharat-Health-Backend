# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Appointments(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('Patients', models.DO_NOTHING, blank=True, null=True)
    doctor = models.ForeignKey('Doctors', models.DO_NOTHING, blank=True, null=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_type = models.CharField(max_length=50, blank=True, null=True)
    appointment_status = models.CharField(max_length=9)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointments'


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
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
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
    action_flag = models.PositiveSmallIntegerField()
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


class Doctors(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100)
    middle_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=6)
    dob=models.DateField()
    primary_address=models.CharField(max_length=255,blank=True,null=True)
    secondary_address=models.CharField(max_length=255,blank=True,null=True)
    state= models.CharField(max_length=255, blank=True, null=True)
    city=models.CharField(max_length=255,blank=True,null=True)
    pin_code=models.IntegerField(blank=True,null=True)
    gmail = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    phone_no = models.CharField(unique=True, max_length=15)
    token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'doctors'


class MedicalPrescriptions(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('Patients', models.DO_NOTHING, blank=True, null=True)
    doctor = models.ForeignKey(Doctors, models.DO_NOTHING, blank=True, null=True)
    bp_s = models.IntegerField(blank=True, null=True)
    bp_d = models.IntegerField(blank=True, null=True)
    saturation = models.IntegerField(blank=True, null=True)
    pulse_rate = models.IntegerField(blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    map = models.DecimalField(db_column='MAP', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    symptoms = models.TextField(blank=True, null=True)
    pmh = models.TextField(db_column='PMH', blank=True, null=True)  # Field name made lowercase.
    medication = models.TextField(blank=True, null=True)
    test_lab = models.ForeignKey('TestLabs', models.DO_NOTHING, db_column='test_lab', blank=True, null=True)
    surgery_recommendation = models.CharField(max_length=255, blank=True, null=True)
    surgery_type = models.CharField(max_length=255, blank=True, null=True)
    reason_for_surgery = models.TextField(blank=True, null=True)
    followup = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'medical_prescriptions'


class Patients(models.Model):
    patient_id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100)
    middle_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=6)
    dob=models.DateField()
    primary_address=models.CharField(max_length=255,blank=True,null=True)
    secondary_address=models.CharField(max_length=255,blank=True,null=True)
    state= models.CharField(max_length=255, blank=True, null=True)
    city=models.CharField(max_length=255,blank=True,null=True)
    pin_code=models.IntegerField(blank=True,null=True)
    gmail = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    phone_no = models.CharField(unique=True, max_length=15)
    token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'patients'


class TestLabs(models.Model):
    lab_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True, null=True)
    gmail = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    contact_no = models.CharField(unique=True, max_length=15)

    class Meta:
        managed = False
        db_table = 'test_labs'


class TestRequests(models.Model):
    test_request_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patients, models.DO_NOTHING, blank=True, null=True)
    test_lab_no = models.ForeignKey(TestLabs, models.DO_NOTHING, db_column='test_lab_no', blank=True, null=True)
    test_type = models.CharField(max_length=100, blank=True, null=True)
    test_date = models.DateField()
    test_time = models.TimeField()
    test_status = models.CharField(max_length=9)
    results = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    requested_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_requests'


class PermissionPatientDoctor(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    is_allowed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('patient', 'doctor')
        db_table="permission_patient_doctor"
        managed=False