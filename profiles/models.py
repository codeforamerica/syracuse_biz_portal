from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    checklists = models.ManyToManyField('biz_content.Checklist')
    checked_items = models.ManyToManyField('biz_content.ChecklistItem')
