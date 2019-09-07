from django import template

register = template.Library()


def startswith(text, value):
    try:
        return text.startswith(value)
    except AttributeError:
        return False


register.filter('startswith', startswith)
