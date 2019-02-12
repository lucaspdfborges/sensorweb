from django import template

register = template.Library()

@register.filter(name='short_name')
def short_name(value):
    st1 = value.split()
    st2 = st1[0] + " " + st1[-1]
    return st2

@register.filter(name='formatDateTime')
def formatDateTime(value):
    return value.strftime("%H:%M:%S %d/%m/%Y")

@register.filter(name='hasData')
def hasData(exp):
    if exp.created>exp.last_seen:
        return False
    else:
        return True
