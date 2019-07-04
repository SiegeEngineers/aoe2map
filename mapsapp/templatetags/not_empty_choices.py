from django import template

register = template.Library()


def not_empty_choices(value):
    try:
        return value.choices != []
    except AttributeError:
        return True


register.filter('not_empty_choices', not_empty_choices)
