from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def format_10_digit_phone(digits):
    phone_tuple = (digits[0:3], digits[3:6], digits[6:])
    return '%s-%s-%s' % phone_tuple
