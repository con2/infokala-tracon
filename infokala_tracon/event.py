from django.conf import settings
from django.http import Http404

from collections import namedtuple

import requests


Event = namedtuple('Event', 'slug name')


_event_cache = {}
def get_event_or_404(slug):
    if slug in _event_cache:
        event = _event_cache[slug]
    else:
        event_url = settings.KOMPASSI_API_V2_EVENT_INFO_URL_TEMPLATE.format(
            kompassi_host=settings.KOMPASSI_HOST,
            event_slug=slug,
        )

        response = requests.get(event_url)

        if response.status_code == 200:
            # Cache positive response
            event_json = response.json()
            event = _event_cache[slug] = Event(event_json['slug'], event_json['name'])
        elif response.status_code == 404:
            # Cache negative response
            event = _event_cache[slug] = None
        else:
            response.raise_for_status()
            raise ValueError('This should not happen (status code {})'.format(response.status_code))

    if event is None:
        raise Http404('Event not found: {}'.format(slug))

    return event
