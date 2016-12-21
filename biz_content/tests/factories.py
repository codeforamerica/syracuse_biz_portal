import factory
import os

from django.conf import settings
from django.utils import timezone
from factory import django as dfactory


class UserFactory(dfactory.DjangoModelFactory):

    class Meta:
        model = 'auth.User'

    username = factory.Sequence(lambda n: "user_%03d" % n)
    email = factory.Sequence(lambda n: "user_%03d@email.com" % n)
    first_name = 'Johnny'
    last_name = factory.Sequence(lambda n: "%03d" % n)


class ProjectFactory(dfactory.DjangoModelFactory):

    class Meta:
        model = 'biz_content.Project'

    name = 'Name'


class ChecklistItemFactory(dfactory.DjangoModelFactory):

    class Meta:
        model = 'biz_content.ChecklistItem'

    text = factory.Sequence(lambda n: "This is checkbox label: %03d" % n)


class StepPageFactory(dfactory.DjangoModelFactory):

    class Meta:
        model = 'biz_content.StepPage'

    title = factory.sequence(lambda n: "%03d" % n)
    slug = factory.Sequence(lambda n: "%03d" % n)
    description = factory.Sequence(lambda n: "%03d" % n)
    depth = 1
    path = 'test'
    checklist_item1 = factory.RelatedFactory(
        ChecklistItemFactory, 'checklist')
    checklist_item2 = factory.RelatedFactory(
        ChecklistItemFactory, 'checklist')
