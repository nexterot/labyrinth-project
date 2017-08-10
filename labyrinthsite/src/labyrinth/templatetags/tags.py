from django import template

register = template.Library()


@register.filter('typename')
def typename(object):
    return object.__class__.__name__

