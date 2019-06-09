from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.


from .models import DpMitglieder,DpFunktion


class FunctionInline(admin.TabularInline):
    model = DpFunktion.mitglied.through
    extra = 1


class AdminInline(admin.TabularInline):
    model = DpMitglieder.isadmin.through
    extra = 1


class MitgliedAdmin(admin.ModelAdmin):
    inlines = (FunctionInline,AdminInline)
    list_display = ('name', 'bereitschaft','email','telefon','bemerkung','not_locked','not_inactive')
    list_filter = ['bereitschaft']
    search_fields = ['name']

    def get_ordering(self, request):
        return ['name']  # sort case insensitive


admin.site.register(DpMitglieder,MitgliedAdmin)
