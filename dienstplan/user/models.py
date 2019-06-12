from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class DpAdmin(models.Model):
    user = models.ForeignKey('DpMitglieder', models.DO_NOTHING, db_column='user')
    dienstplan = models.ForeignKey('dienste.DpDienstplan', models.DO_NOTHING, db_column='dienstplan')
    email_neu = models.IntegerField()
    email_austragen = models.IntegerField()
    email_uebernahme = models.IntegerField()
    email_adminaction = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dp_admin'


class DpBereitschaft(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'dp_bereitschaft'


class DpMitglieder(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    bereitschaft = models.ForeignKey(DpBereitschaft, models.DO_NOTHING, db_column='bereitschaft')
    berufer = models.IntegerField()
    steuer = models.BooleanField();
    lastlogin = models.IntegerField()
    login = models.CharField(max_length=255, blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=255, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    newpasshash = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    telefon = models.CharField(max_length=255, blank=True, null=True)
    bemerkung = models.CharField(max_length=255, blank=True, null=True)
    pnr = models.CharField(max_length=8, blank=True, null=True)
    sid = models.CharField(max_length=255, blank=True, null=True)
    startdp = models.ForeignKey('dienste.DpDienstplan', models.DO_NOTHING, db_column='startdp',related_name='+')
    seeuserdetails = models.IntegerField(db_column='seeUserDetails', blank=True, null=True)  # Field name made lowercase.
    seestatistics = models.IntegerField(db_column='seeStatistics', blank=True, null=True)  # Field name made lowercase.
    rightswachbuch = models.IntegerField(db_column='rightsWachbuch', blank=True, null=True)  # Field name made lowercase.
    tagewachbuch = models.IntegerField(db_column='tageWachbuch')  # Field name made lowercase.
    wronglogin = models.IntegerField()
    locked = models.BooleanField()
    inactive = models.BooleanField()
    be_login = models.CharField(max_length=255, blank=True, null=True)
    be_pass = models.CharField(max_length=255, blank=True, null=True)
    kvadmin = models.IntegerField()
    ad_user = models.CharField(max_length=30, blank=True, null=True)
    ad_initialpasswort = models.CharField(max_length=10, blank=True, null=True)
    kontodatenvorhanden = models.IntegerField()
    created = models.DateTimeField()
    isadmin = models.ManyToManyField('dienste.DpDienstplan',through=DpAdmin)
    authid = models.OneToOneField(User, on_delete=models.CASCADE, db_column='authid')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            DpMitglieder.objects.create(authid=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.dpmitglieder.save()


    name.admin_order_field = 'name'

    def not_locked(self):
        return not self.locked

    def not_inactive(self):
        return not self.inactive

    not_locked.boolean = True
    not_inactive.boolean = True
    not_locked.admin_order_field = 'locked'
    not_inactive.admin_order_field = 'inactive'

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'dp_mitglieder'


class DpFunktionsvk(models.Model):
    mitglied = models.ForeignKey('DpMitglieder', models.DO_NOTHING, db_column='mitglied')
    funktion = models.ForeignKey('DpFunktion', models.DO_NOTHING, db_column='funktion')

    class Meta:
        managed = False
        db_table = 'dp_funktionsVK'


class DpFunktion(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    dienstplan = models.ForeignKey('dienste.DpDienstplan', models.DO_NOTHING, db_column='dienstplan')
    order = models.IntegerField()
    wachgeld = models.DecimalField(max_digits=6, decimal_places=2)
    wachgeld_art = models.IntegerField()
    wachgeld_kat = models.CharField(max_length=2, blank=True, null=True)
    ical_alarm = models.IntegerField()
    mitglied = models.ManyToManyField(DpMitglieder, through=DpFunktionsvk)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'dp_funktion'
