# encoding: utf-8

from django.core.management.base import BaseCommand, CommandError


def setup_basic_workflow(event_slug):
    from infokala.models import Workflow, State, MessageType, Message

    basic_workflow, unused = Workflow.objects.get_or_create(
        name=u'Perustyönkulku',
    )

    lost_and_found_workflow, unused = Workflow.objects.get_or_create(
        name=u'Löytötavaratyönkulku',
    )

    simple_workflow, unused = Workflow.objects.get_or_create(
        name=u'Yksinkertainen työnkulku',
    )

    order = 0
    for workflow, name, slug, initial, label_class, active in [
        (basic_workflow, u'Avoinna', 'open', True, 'label-primary', True),
        (basic_workflow, u'Hoidettu', 'resolved', False, 'label-success', False),

        (lost_and_found_workflow, u'Kateissa', 'missing', True, 'label-primary', True),
        (lost_and_found_workflow, u'Tuotu Infoon', 'found', False, 'label-info', True),
        (lost_and_found_workflow, u'Palautettu omistajalle', 'returned', False, 'label-success', False),

        (simple_workflow, u'Kirjattu', 'recorded', True, 'label-primary', True),
    ]:
        state, created = State.objects.get_or_create(
            workflow=workflow,
            slug=slug,
            defaults=dict(
                name=name,
                order=order,
                initial=initial,
            ),
        )

        state.label_class = label_class
        state.active = active
        state.save()

        order += 10

    for name, slug, workflow in [
        (u'Löytötavarat', 'lost-and-found', lost_and_found_workflow),
        (u'Tehtävä', 'task', basic_workflow),
        (u'Lokikirja', 'event', simple_workflow),
    ]:
        message_type, unused = MessageType.objects.get_or_create(
            event_slug=event_slug,
            slug=slug,
            defaults=dict(
                name=name,
                workflow=workflow,
            ),
        )

    # make 'event' default
    message_type.default = True
    message_type.save()


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('event_slugs', nargs='+', type=unicode)

    def handle(self, *args, **opts):
        for event_slug in opts['event_slugs']:
            print 'Setting up basic workflow for event', event_slug
            setup_basic_workflow(event_slug)
