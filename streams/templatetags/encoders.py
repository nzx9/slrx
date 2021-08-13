from django import template
import urllib.parse

register = template.Library()


@register.filter
def uriencode(value):
    value = urllib.parse.quote(value)
    return value.replace("/", "%2F")
