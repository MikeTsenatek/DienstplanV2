from django import template
import sys
from dienste.models import DpDienstplan

register = template.Library()

@register.simple_tag
def getdienstplan():
    print("getdienstplan", file=sys.stderr)

    return DpDienstplan.objects.filter(inactive=0).order_by('order')
