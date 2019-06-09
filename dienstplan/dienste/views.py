from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import DpDienste,DpBesatzung,DpDienstplanFelder


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'dienste/index.html'
    context_object_name = 'dienste_list'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user'] = self.request.user
        return data

    def get_queryset(self):
        return DpDienste.objects.filter(ordner=1108).select_related('schicht').prefetch_related('besatzung__personal').select_related('schicht__wagenart')

