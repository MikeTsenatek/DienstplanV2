from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from .models import DpDienste,DpBesatzung,DpDienstplan,DpOrdner


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'dienste/index.html'
    context_object_name = 'dienste_list'

    dienstplanid = ''

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user'] = self.request.user
        data['ordner'] = DpOrdner.objects.filter(Q(dienstplan=self.dienstplanid) & Q(lock__lt = 3)).order_by('-jahr','-monat_uint')

        return data

    def get_queryset(self, ):
        if 'dienstplanid' in self.kwargs:
            self.dienstplanid = int(self.kwargs['dienstplanid']);
        else:
            self.dienstplanid = int(self.request.user.dpmitglieder.startdp)

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

