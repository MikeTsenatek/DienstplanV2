from django.contrib import admin

# Register your models here.

from .models import DpDienste,DpBesatzung


class BesatzungInline(admin.TabularInline):
    model = DpBesatzung
    extra = 0


class DiensteAdmin(admin.ModelAdmin):
    list_display = ('tag', 'schicht', 'ordner', 'ordner_name')
    list_filter = ('ordner__dienstplan', 'ordner__jahr', 'ordner__monat', 'tag')
    inlines = [BesatzungInline]


admin.site.register(DpDienste, DiensteAdmin)
