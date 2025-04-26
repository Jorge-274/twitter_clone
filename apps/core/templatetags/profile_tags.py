from django import template
from django.conf import settings
import os

register = template.Library()

@register.simple_tag
def profile_or_default(profile_picture):
    if profile_picture and getattr(profile_picture, 'name', None):
        return profile_picture.url
    return os.path.join(settings.STATIC_URL, 'images/default.png')
