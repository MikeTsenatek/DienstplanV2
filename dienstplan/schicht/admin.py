from django.contrib import admin

from .models import DpSchicht


# Register your models here.


class SchichtAdmin(admin.ModelAdmin):
    list_display = ('dienstplan', 'wache','wagenart','start','dauer','comment','order', 'isinactive', 'wachbuchenabled')
    list_filter = ['dienstplan','wache','wagenart','wachbuch','inactive']


admin.site.register(DpSchicht, SchichtAdmin)
