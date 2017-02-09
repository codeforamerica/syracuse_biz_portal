import xml.etree.ElementTree

from django import template
from django.template.defaultfilters import stringfilter
from biz_content import choices


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


@register.filter
@stringfilter
def display_inspection_type_name(inspection_type):
    return choices.INSPECTION_TYPE_CHOICES[inspection_type]


@register.filter
@stringfilter
def display_inspection_department_type(inspection_type):
    return choices.INSPECTION_DEPARTMENT_CHOICES[inspection_type]


@register.filter
@stringfilter
def display_status_type_name(status):
    return choices.INSPECTION_STATUS_CHOICES[status]


@register.filter
@stringfilter
def display_inspection_status_icon(status):
    return INSPECTION_ICON_CHOICES[status]


@register.filter
@stringfilter
def retrieve_payment_details(payment_details):
    root = xml.etree.ElementTree.fromstring(payment_details)
    payment = root.find('Payment_Type')
    payment_info = payment.items()
    payer = payment_info[0][1]
    return '%s paid ' % (payer,)


@register.filter
@stringfilter
def display_permit_type_name(status):
    return choices.PERMIT_TYPE_CHOICES[status]


@register.filter
@stringfilter
def display_permit_dpt_name(dpt):
    return choices.PERMIT_DEPARTMENT_CHOICES[dpt]
