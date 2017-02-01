from django import template
from django.template.defaultfilters import stringfilter
import xml.etree.ElementTree


register = template.Library()

INSPECTION_TYPE_CHOICES = {'85': 'Codes Inspection (Electrical)',
                           '84': 'Codes Inspection (Building)',
                           '83': 'Fire Prevention Inspection',
                           '82': 'Zoning Inspection'
                           }

INSPECTION_DEPARTMENT_CHOICES = {'85': 'Codes',
                                 '84': 'Codes',
                                 '83': 'Fire'
                                 }

INSPECTION_STATUS_CHOICES = {'1': 'Pass',
                             '2': 'Fail',
                             '3': 'N/A',
                             '4': 'In Progress',
                             '5': 'No Progress',
                             '6': 'No Work Started'
                             }


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
def display_inspection_department_type(inspection_type):
    return INSPECTION_DEPARTMENT_CHOICES[inspection_type]


@register.filter
@stringfilter
def display_status_type_name(status):
    return INSPECTION_STATUS_CHOICES[status]


@register.filter
@stringfilter
def retrieve_payment_details(payment_details):
    root = xml.etree.ElementTree.fromstring(payment_details)
    payment = root.find('Payment_Type')
    payment_info = payment.items()
    amount = payment_info[1][1]
    payer = payment_info[0][1]
    return '%s paid $%s' % (payer, amount)
