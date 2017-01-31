from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

INSPECTION_TYPE_CHOICES = {'85': 'Codes Inspection (Electrical)',
                           '84': 'Codes Inspection (Building)',
                           '83': 'Fire Prevention Inspection',
                           '82': 'Zoning Inspection'}

INSPECTION_STATUS_CHOICES = {'1': 'Pass',
                             '2': 'Fail',
                             '3': 'N/A',
                             '4': 'In Progress',
                             '5': 'In Progress',
                             '6': 'No Work Started'}


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


@register.filter
@stringfilter
def display_inspection_type_name(inspection_type):
    return INSPECTION_TYPE_CHOICES[inspection_type]


@register.filter
@stringfilter
def display_status_type_name(status):
    return INSPECTION_STATUS_CHOICES[status]
