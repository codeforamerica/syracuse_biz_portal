import datetime
import factory
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


class StepPageFactory(dfactory.DjangoModelFactory):
    title = factory.sequence(lambda n: "%03d" % n)
    slug = factory.Sequence(lambda n: "%03d" % n)
    description = factory.Sequence(lambda n: "%03d" % n)
    date = factory.LazyFunction(datetime.datetime.utcnow)
    depth = 1
    path = 'test'
    checklist_item1 = factory.RelatedFactory(
                            ChecklistItemFactory, 'checklist_items')
    class Meta:
        model = 'biz_content.StepPage'


class ChecklistItemFactory(dfactory.DjangoModelFactory):
    date = factory.LazyFunction(datetime.datetime.utcnow)

    class Meta:
        model = 'biz_content.ChecklistItem'
