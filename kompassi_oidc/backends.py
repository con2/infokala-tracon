from django.conf import settings
from django.contrib.auth.models import Group
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class KompassiOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    """
    Signs users in with Kompassi OIDC and mirrors their Kompassi groups on every login.

    Accounts created by the legacy OAuth2 flow are found by email, which Kompassi sends and those
    accounts already have. Access to each event is decided later from the mirrored groups, see
    `infokala_tracon.views.is_user_allowed_to_access`, so any Kompassi user may sign in.
    """

    def create_user(self, claims):
        # The base class only creates the row; update_user is not called for new users.
        return self.update_user(super().create_user(claims), claims)

    def update_user(self, user, claims):
        groups = claims.get("groups", [])
        is_admin = settings.KOMPASSI_ADMIN_GROUP in groups

        user.email = claims.get("email", user.email)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.is_superuser = is_admin
        user.is_staff = is_admin
        user.save()
        user.groups.set([Group.objects.get_or_create(name=name)[0] for name in groups])

        return user
