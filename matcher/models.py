from django.db import models
from django.utils.translation import ugettext as _
from wealthmap.models import Opportunity


class Opportunity(Opportunity):
    description = models.TextField()
    value_prop = models.CharField(max_length=255,
                                  null=False,
                                  blank=False,
                                  verbose_name=_('outcome'),
                                  help_text=_('e.g. loan, 30hrs of mentoring'))
    application_link = models.TextField()

    class Meta:
        verbose_name = _('Opportunity')
        verbose_name_plural = _('Opportunities')
