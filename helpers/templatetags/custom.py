from django import template

from helpers.utils import Encryption

register = template.Library()


@register.filter
def bootstrap_level_tag_map(value):
    bootstrap_level_tags = {
        'debug': 'dark',
        'info': 'info',
        'success': 'success',
        'warning': 'warning',
        'error': 'danger',
    }
    return bootstrap_level_tags[value]


@register.filter
def encrypt(value):
    return Encryption.encrypt(value)


@register.filter
def decrypt(value):
    return Encryption.decrypt(value)
