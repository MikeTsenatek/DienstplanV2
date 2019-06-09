from django.db import models
import datetime

# Create your models here.

class DpWache(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    dienstplan = models.ForeignKey('dienste.DpDienstplan', models.DO_NOTHING, db_column='dienstplan')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'dp_wache'


class DpWagenart(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    dienstplan = models.ForeignKey('dienste.DpDienstplan', models.DO_NOTHING, db_column='dienstplan')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'dp_wagenart'


class DpSchicht(models.Model):
    dienstplan = models.ForeignKey('dienste.DpDienstplan', models.DO_NOTHING, db_column='dienstplan')
    wache = models.ForeignKey('DpWache', models.DO_NOTHING, db_column='wache')
    start = models.TimeField()
    dauer = models.TimeField()
    wagenart = models.ForeignKey('DpWagenart', models.DO_NOTHING, db_column='wagenart')
    order = models.IntegerField()
    inactive = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True, null=True)
    wachbuch = models.IntegerField()
    wachbuch.boolean = True
    wachbuch.admin_order_field = 'wachbuch'

    def bis(self):
        stunde_neu = self.start.hour + self.dauer.hour
        minute_neu = self.start.minute + self.dauer.minute

        if minute_neu >= 60:
            minute_neu = minute_neu -60
            stunde_neu = stunde_neu - 1

        if stunde_neu >= 24:
            stunde_neu = stunde_neu -24

        return datetime.time(stunde_neu,minute_neu,0)

    def isinactive(self):
        return self.inactive

    isinactive.boolean = True
    isinactive.admin_order_field = 'inactive'

    def wachbuchenabled(self):
        return self.wachbuch

    wachbuchenabled.boolean = True
    wachbuchenabled.admin_order_field = 'inactive'

    def __str__(self):
        return self.dienstplan.name + " " + self.wagenart.name + " " + str(self.start)

    class Meta:
        managed = False
        db_table = 'dp_schicht'
