from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView

from .views import (
    ConfigView,
    logout_view,
    MessagesView,
    MessageView,
    MessageEventsView,
    slash_redirect_view,
    static_app_view,
    status_view,
)
from django.urls import path, re_path

urlpatterns = [
    # XXX hardcoded
    path('', RedirectView.as_view(url='/events/{default_event}/messages'.format(default_event=settings.INFOKALA_DEFAULT_EVENT)),
        name='infokala_frontpage_redirect_view',
    ),
    re_path(r'^events/(?P<event_slug>[a-z0-9-]+)/messages/$', static_app_view),
    re_path(r'^events/[a-z0-9-]+/messages$', slash_redirect_view),
    re_path(r'^events/(?P<event_slug>[a-z0-9-]+)/messages/config.js$',
        csrf_exempt(ConfigView.as_view()),
        name='infokala_config_view',
    ),
    re_path(r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/messages/?$',
        csrf_exempt(MessagesView.as_view()),
        name='infokala_messages_view',
    ),
    re_path(r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/messages/(?P<message_id>\d+)/?$',
        csrf_exempt(MessageView.as_view()),
        name='infokala_message_view',
    ),
    re_path(r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/messages/(?P<message_id>\d+)/events/?$',
        csrf_exempt(MessageEventsView.as_view()),
        name='infokala_message_events_view',
    ),

    re_path(r'^api/v1/status/?$', status_view, name='status_view'),


    path('admin/', admin.site.urls),
    re_path(r'^logout/?$', logout_view),
    path('', include('kompassi_oauth2.urls')),
]
