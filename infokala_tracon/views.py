from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.views import serve
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from infokala.views import (
    ConfigView as InfokalaConfigView,
)
from infokala.views import (
    MessageEventsView as InfokalaMessageEventsView,
)
from infokala.views import (
    MessagesView as InfokalaMessagesView,
)
from infokala.views import (
    MessageView as InfokalaMessageView,
)


def is_user_allowed_to_access(user, event):
    if user.is_superuser:
        return True

    group_names = [
        tmpl.format(
            kompassi_installation_slug=settings.KOMPASSI_INSTALLATION_SLUG,
            infokala_installation_slug=settings.INFOKALA_INSTALLATION_SLUG,
            event_slug=event.slug,
        )
        for tmpl in settings.INFOKALA_ACCESS_GROUP_TEMPLATES
    ]
    group_names.append(settings.KOMPASSI_ADMIN_GROUP)
    return user.groups.filter(name__in=group_names).exists()


class AccessControlMixin(object):
    def authenticate(self, request, event):
        return is_user_allowed_to_access(request.user, event)


class MessagesView(AccessControlMixin, InfokalaMessagesView):
    pass


class MessageView(AccessControlMixin, InfokalaMessageView):
    pass


class MessageEventsView(AccessControlMixin, InfokalaMessageEventsView):
    pass


class ConfigView(AccessControlMixin, InfokalaConfigView):
    pass


@login_required
def static_app_view(request, event_slug):
    event = settings.INFOKALA_GET_EVENT_OR_404(slug=event_slug)

    if not is_user_allowed_to_access(request.user, event):
        return render(request, "infokala_tracon_forbidden.html", status=403)

    return serve(request, path="infokala/infokala.html", insecure=True)


def slash_redirect_view(request):
    return redirect(request.path + "/")


def logout_view(request):
    logout(request)

    next_page = request.GET.get("next", settings.LOGOUT_REDIRECT_URL)
    return redirect(next_page)


def status_view(request):
    return JsonResponse({"status": "OK"})


def default_event_redirect_view(request):
    from infokala.models import MessageType

    message_type = MessageType.objects.latest("id")
    return redirect("infokala_messages_view", event_slug=message_type.event_slug)
