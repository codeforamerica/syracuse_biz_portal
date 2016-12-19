import factory
from django.utils import timezone
from factory import django as dfactory


class UserFactory(dfactory.DjangoModelFactory):
    username = factory.Sequence(lambda n: "user_%03d" % n)
    email = factory.Sequence(lambda n: "user_%03d@email.com" % n)
    first_name = 'Johnny'
    last_name = factory.Sequence(lambda n: "%03d" % n)

    class Meta:
        model = 'auth.User'


class ProjectFactory(dfactory.DjangoModelFactory):

    class Meta:
        model = 'biz_content.Project'

    name = 'Name'
    owner = factory.SubFactory(UserFactory)


class ChecklistItemFactory(dfactory.DjangoModelFactory):
    text = factory.Sequence(lambda n: "This is checkbox label: %03d" % n)

    class Meta:
        model = 'biz_content.ChecklistItem'


class StepPageFactory(dfactory.DjangoModelFactory):
    title = factory.sequence(lambda n: "%03d" % n)
    slug = factory.Sequence(lambda n: "%03d" % n)
    description = factory.Sequence(lambda n: "%03d" % n)
    depth = 1
    path = 'test'
    checklist_item1 = factory.RelatedFactory(
        ChecklistItemFactory, 'checklist')
    checklist_item2 = factory.RelatedFactory(
        ChecklistItemFactory, 'checklist')

    class Meta:
        model = 'biz_content.StepPage'
