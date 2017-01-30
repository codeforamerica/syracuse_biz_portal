from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def format_10_digit_phone(digits):
    phone_tuple = (digits[0:3], digits[3:6], digits[6:])
    return '%s-%s-%s' % phone_tuple


@register.filter
@stringfilter
def format_business_license_date(date):
    d = date[0:][:10]
    date = d.split('-')
    year = date[0]
    month = date[1]
    day = date[2]
    string = month + '/' + day + '/' + year
    return string
