from django import template
from datetime import date

register = template.Library()

@register.filter
def status_color(value):
    value = value.lower() if value else ''
    if value == 'realizada':
        return 'success'
    elif value == 'pendente':
        return 'warning'
    elif value == 'nao_realizada':
        return 'danger'
    return 'secondary'

@register.filter
def is_coleta_atrasada(coleta):
    return coleta.status_coleta == "PENDENTE" and coleta.data_coleta < date.today()

@register.filter
def is_entrega_atrasada(coleta):
    return coleta.status_entrega == "PENDENTE" and coleta.data_coleta < date.today()