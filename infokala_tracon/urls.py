from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView

from .views import (
    ConfigView,
    logout_view,
    MessagesView,
    MessageView,
    slash_redirect_view,
    static_app_view,
)

urlpatterns = patterns('',
    # XXX hardcoded
    url(r'^$',
        RedirectView.as_view(url='/events/hitpoint2015/messages'),
        name='infokala_frontpage_redirect_view',
    ),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/messages/$', static_app_view),
    url(r'^events/[a-z0-9-]+/messages$', slash_redirect_view),
    url(r'^events/(?P<event_slug>[a-z0-9-]+)/messages/config.js$',
        csrf_exempt(ConfigView.as_view()),
        name='infokala_config_view',
    ),
    url(r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/messages/?$',
        csrf_exempt(MessagesView.as_view()),
        name='infokala_messages_view',
    ),
    url(r'^api/v1/events/(?P<event_slug>[a-z0-9-]+)/messages/(?P<message_id>\d+)/?$',
        csrf_exempt(MessageView.as_view()),
        name='infokala_message_view',
    ),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/?$', logout_view),
    url(r'', include('kompassi_oauth2.urls')),
)
