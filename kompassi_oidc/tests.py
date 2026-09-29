from unittest import mock

from django.contrib.auth.models import Group, User
from django.test import TestCase, override_settings

from .backends import KompassiOIDCAuthenticationBackend


def claims(**overrides):
    return {
        "sub": "1234",
        "email": "mahti@example.com",
        "given_name": "Markku",
        "family_name": "Mahtinen",
        "groups": ["turska-tracon2026-labour-info"],
        **overrides,
    }


@override_settings(KOMPASSI_ADMIN_GROUP="admins")
class KompassiOIDCAuthenticationBackendTestCase(TestCase):
    def sign_in(self, user_info):
        backend = KompassiOIDCAuthenticationBackend()
        with mock.patch.object(backend, "get_userinfo", return_value=user_info):
            return backend.get_or_create_user("access token", "id token", {})

    def test_legacy_account_is_reattached_by_email(self):
        # Created by the legacy OAuth2 flow, which used the Kompassi username.
        legacy = User.objects.create_user("mahti", email="Mahti@Example.com")

        user = self.sign_in(claims())

        self.assertEqual(user.pk, legacy.pk)
        self.assertEqual(user.username, "mahti")
        self.assertEqual(User.objects.count(), 1)

    def test_new_account_gets_groups_on_first_sign_in(self):
        user = self.sign_in(claims(groups=["admins", "turska-tracon2026-labour-jv"]))

        self.assertEqual(user.first_name, "Markku")
        self.assertEqual(user.last_name, "Mahtinen")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(
            set(user.groups.values_list("name", flat=True)),
            {"admins", "turska-tracon2026-labour-jv"},
        )

    def test_losing_groups_in_kompassi_revokes_them_on_next_sign_in(self):
        self.sign_in(claims(groups=["admins", "turska-tracon2026-labour-info"]))

        user = self.sign_in(claims(groups=[]))

        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.groups.exists())
        # The Group rows stay for other members.
        self.assertTrue(Group.objects.filter(name="admins").exists())
