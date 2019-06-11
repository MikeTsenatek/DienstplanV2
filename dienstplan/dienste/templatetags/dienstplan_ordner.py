from django import template
from dienste.models import DpOrdner, DpDienstplan

register = template.Library()

@register.simple_tag
def getdienstplanordner():
    returnvar = {}
    for item in DpOrdner.objects.filter(lock=0):
        if item.dienstplan.id not in returnvar:
            returnvar[item.dienstplan.id] = {}

        if item.jahr not in returnvar[item.dienstplan.id]:
            returnvar[item.dienstplan.id][item.jahr] = {}

        returnvar[item.dienstplan.id][item.jahr][item.monat] = item

    return returnvar

@register.simple_tag
def getdienstplan():
    return DpDienstplan.objects.filter(inactive=0).order_by('order')
