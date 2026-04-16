from django import template
from app.models import Tovar

register = template.Library()

@register.filter
def get_tovar(tovar_id):
    try:
        return Tovar.objects.get(id=tovar_id)
    except Tovar.DoesNotExist:
        return None

@register.filter
def multiply(value, arg):
    return value * arg