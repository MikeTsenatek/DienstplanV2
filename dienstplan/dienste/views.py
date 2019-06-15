# Create your views here.
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.views import generic

from user.models import DpFunktion
from .models import DpDienste, DpDienstplan, DpOrdner


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'dienste/index.html'
    context_object_name = 'dienste_list'

    dienstplanid = ''

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user'] = self.request.user
        data['ordner'] = DpOrdner.objects.filter(Q(dienstplan=self.dienstplanid) & Q(lock__lt = 3)).order_by('-jahr','-monat_uint')
        data['admin'] = DpDienstplan.objects.filter(id=self.dienstplanid)[:1].get().isadmin(self.request.user)
        data['funktionen'] = DpFunktion.objects.all()
        return data

    def get_queryset(self, ):
        if 'dienstplanid' in self.kwargs:
            self.dienstplanid = int(self.kwargs['dienstplanid']);
        else:
            self.dienstplanid = self.request.user.dpmitglieder.startdp.id

        if 'ordnerid' in self.kwargs:
            ordnerid = self.kwargs['ordnerid']
        else:
            today = datetime.date.today()

            ordnerid = DpOrdner.objects.filter((Q(monat_uint__lte=today.month) & Q(jahr=today.year) | Q(jahr__lt=today.year))
                                               & Q(dienstplan=self.dienstplanid) & Q(lock__lt = 3)).order_by('-jahr','-monat_uint')[:1].get().ordnerid

        if DpDienstplan.objects.filter(id=self.dienstplanid)[:1].get().hasAccess(self.request.user):
            return DpDienste.objects.filter(ordner=ordnerid).select_related('schicht').\
            prefetch_related('besatzung__personal').select_related('schicht__wagenart')
        else:
            raise PermissionDenied('You are not allowed to view this plan')



def userbyfunktion(request, funktionid, name):

    return JsonResponse(list(DpFunktion.objects.filter(Q(id=funktionid) & Q(mitglied__name__startswith=name)).values_list(
        'mitglied__name')), safe=False)
