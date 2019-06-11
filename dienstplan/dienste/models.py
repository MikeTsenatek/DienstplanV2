# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import datetime


class DpBesatzung(models.Model):
    dienst = models.ForeignKey('DpDienste', models.DO_NOTHING, db_column='dienst',related_name='besatzung')
    art = models.ForeignKey('DpDienstplanFelder', models.DO_NOTHING, db_column='art')
    funktionart = models.ForeignKey('user.DpFunktion',models.DO_NOTHING,db_column='funktionart')
    berufer = models.IntegerField(blank=True, null=True)
    optional = models.IntegerField()
    personal = models.ForeignKey('user.DpMitglieder', models.DO_NOTHING, db_column='personal', blank=True, null=True)
    freigegeben = models.IntegerField()
    bemerkung = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'dp_besatzung'
        ordering = ['art__order']


class DpDienste(models.Model):
    tag = models.CharField(max_length=2, blank=True, null=True)
    schicht = models.ForeignKey('schicht.DpSchicht',models.DO_NOTHING,db_column='schicht')
    bemerkung = models.CharField(max_length=255, blank=True, null=True)
    bemerkung2 = models.CharField(max_length=255, blank=True, null=True)
    ordner = models.ForeignKey('DpOrdner', models.DO_NOTHING, db_column='ordner')
    besatzung = DpBesatzung.objects.all().prefetch_related('besatzung')

    def ordner_name(self):
        return self.ordner.name

    def calenderweek(self):
        return datetime.date(self.ordner.jahr, self.ordner.monat_uint,  int(self.tag )).isocalendar()[1]

    class Meta:
        managed = False
        db_table = 'dp_dienste'
        ordering = ['tag','schicht__order']


class DpDienstplan(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    showwagenfilter = models.IntegerField()
    showwachenfilter = models.IntegerField()
    order = models.IntegerField()
    inactive = models.IntegerField()
    viewable = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'dp_dienstplan'


class DpDienstplanFelder(models.Model):
    dienstplan = models.ForeignKey(DpDienstplan, models.DO_NOTHING, db_column='dienstplan')
    name = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'dp_dienstplan_felder'


class DpLog(models.Model):
    besatzungsid = models.ForeignKey(DpBesatzung, models.DO_NOTHING, db_column='besatzungsid')
    userid = models.ForeignKey('user.DpMitglieder', models.DO_NOTHING, db_column='userid')
    time = models.IntegerField()
    besatzungold = models.IntegerField(blank=True, null=True)
    besatzungnew = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dp_log'


class DpNachricht(models.Model):
    titel = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    time = models.IntegerField()
    user = models.ForeignKey('user.DpMitglieder', models.DO_NOTHING, db_column='user')
    annoucment = models.IntegerField()
    email = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dp_nachricht'


class DpNachrichtUser(models.Model):
    nachricht = models.ForeignKey(DpNachricht, models.DO_NOTHING, db_column='nachricht')
    user = models.ForeignKey('user.DpMitglieder', models.DO_NOTHING, db_column='user')
    gesehn = models.IntegerField(blank=True, null=True)
    quittiert = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dp_nachricht_user'


class DpOrdner(models.Model):
    ordnerid = models.AutoField(primary_key=True,db_column='id')
    name = models.CharField(max_length=255, blank=True, null=True)
    monat = models.CharField(max_length=2, blank=True, null=True)
    monat_uint = models.IntegerField(max_length=2,db_column='monat_uint')
    jahr = models.IntegerField()
    dienstplan = models.ForeignKey(DpDienstplan, models.DO_NOTHING, db_column='dienstplan')
    lock = models.IntegerField()
    max = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'dp_ordner'


class DpSetting(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dp_setting'


class DpWachbuch(models.Model):
    besatzung_id = models.IntegerField(blank=True, null=True)
    personal = models.ForeignKey('user.DpMitglieder', models.DO_NOTHING, db_column='personal', related_name='+')
    tag = models.CharField(max_length=2, blank=True, null=True)
    monat = models.CharField(max_length=2, blank=True, null=True)
    jahr = models.CharField(max_length=4, blank=True, null=True)
    start = models.TimeField()
    schichtdauer = models.TimeField()
    arbeitszeit = models.TimeField(blank=True, null=True)
    funktion = models.ForeignKey('user.DpFunktion', models.DO_NOTHING, db_column='funktion')
    wachgeld = models.DecimalField(max_digits=6, decimal_places=2)
    bemerkung = models.CharField(max_length=255, blank=True, null=True)
    time = models.IntegerField()
    verantwortlicher = models.ForeignKey('user.DpMitglieder', models.DO_NOTHING, db_column='verantwortlicher', related_name='+')
    deleted = models.IntegerField(blank=True, null=True)
    deleted_time = models.IntegerField(blank=True, null=True)
    abrechnung = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dp_wachbuch'


class DpWachbuchAbrechnung(models.Model):
    monat = models.IntegerField()
    jahr = models.IntegerField()
    gruppe = models.IntegerField()
    benutzer = models.IntegerField()
    zeit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dp_wachbuch_abrechnung'


class DpWachbuchAusdruck(models.Model):
    time = models.IntegerField()
    user = models.ForeignKey('user.DpMitglieder', models.DO_NOTHING, db_column='user')

    class Meta:
        managed = False
        db_table = 'dp_wachbuch_ausdruck'


class DpWachbuchKat(models.Model):
    name = models.CharField(max_length=5, blank=True, null=True)
    kostenstelle = models.CharField(max_length=11, blank=True, null=True)
    gruppe = models.IntegerField()
    statkat = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'dp_wachbuch_kat'


class DpWbBerechtigung(models.Model):
    user = models.ForeignKey('user.DpMitglieder', models.DO_NOTHING, db_column='user')
    wb_kat = models.ForeignKey(DpWachbuchKat, models.DO_NOTHING, db_column='wb_kat')

    class Meta:
        managed = False
        db_table = 'dp_wb_berechtigung'
