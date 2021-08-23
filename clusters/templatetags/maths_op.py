from django import template

register = template.Library()


@register.filter
def sub(value1, value2):
    return value1 - value2


@register.filter
def add(value1, value2):
    return value1 + value2
