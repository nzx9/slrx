from django import template
import urllib.parse
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def uriencode(value):
    value = urllib.parse.quote(value)
    return value.replace("/", "%2F")


@register.filter
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
