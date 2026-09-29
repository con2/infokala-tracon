# Tracon's deployment of [Infokala]

This is a [Kompassi]-integrated deployment of [Infokala] that authenticates users from Kompassi via OpenID Connect and gets event info from Kompassi using the public API of Kompassi.

[Infokala]: https://github.com/kcsry/infokala "Infokala, the Info Log Management System for Tracon & Desucon"
[Kompassi]: https://github.com/tracon/kompassi "Kompassi, the Tracon Event Management System"

## [Infokala] is installed using `pip`

Note that this repository does not contain the actual source code for the [Infokala] application. The actual application consists of the package called `infokala` that is installed using `pip`.

Please check out a suitable version of Infokala and install it in the same virtualenv using eg. `pip install -e .` (see below).

This repository is responsible for setting up the Tracon/Kompassi specific bits for Infokala, such as the Kompassi OIDC based authentication and group membership based authorization.

## Getting started

First, make sure `kompassi.dev` and `infokala.dev` resolve to localhost via `/etc/hosts`:

    127.0.0.1 localhost kompassi.dev infokala.dev

Next, install and run development instance of [Kompassi] if you don't yet have one:

    virtualenv venv-kompassi
    source venv-kompassi/bin/activate
    git clone https://github.com/tracon/kompassi.git
    cd kompassi
    pip install -r requirements.txt
    ./manage.py setup --test
    ./manage.py runserver 127.0.0.1:8000
    iexplore http://kompassi.dev:8000

`./manage.py setup --test` created a test user account `mahti` with password `mahti` in your Kompassi development instance.

Now, in another terminal, install and run this application:

    virtualenv venv-infokala
    source venv-infokala/bin/activate
    git clone https://github.com/tracon/infokala.git
    cd infokala
    pip install -e .
    cd ..

    git clone https://github.com/tracon/infokala-tracon.git
    cd infokala-tracon
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py infokala_setup_basic_workflow traconx
    ./manage.py runserver 127.0.0.1:8001
    iexplore http://infokala.dev:8001/events/traconx/messages/

## Authentication and authorization

Authentication is performed via OpenID Connect against Kompassi, using [mozilla-django-oidc](https://mozilla-django-oidc.readthedocs.io/) with the backend in `kompassi_oidc/backends.py`. All users that are present in Kompassi are allowed to log in. An account that existed before the move from Kompassi's legacy OAuth2 is matched by email address.

The Kompassi OIDC application needs `RS256` as its algorithm and the redirect URI `https://<hostname>/oidc/callback/`. Its client ID and secret are read from the `KOMPASSI_OAUTH2_CLIENT_ID` and `KOMPASSI_OAUTH2_CLIENT_SECRET` environment variables, the names the legacy OAuth2 client used.

Authorization is performed using the `groups` claim, which is mirrored into Django groups on every login. Groups that grant access to different events' info logs are configurable. The admin group by default grants access to all events.

By default, these are configured as follows:

```python
INFOKALA_ACCESS_GROUP_TEMPLATES = [
    '{kompassi_installation_slug}-{event_slug}-labour-conitea',
    '{kompassi_installation_slug}-{event_slug}-labour-info',
    '{infokala_installation_slug}-{event_slug}-users',
]
INFOKALA_INSTALLATION_SLUG = env('INFOKALA_INSTALLATION_SLUG', default='infokala')
KOMPASSI_INSTALLATION_SLUG = env('KOMPASSI_INSTALLATION_SLUG', default='turska')
```

That would basically grant access to the organizing committee (*conitea*) and info workers.

## Development gotchas

### Applications on `localhost` in different ports share the same cookies

1. Run Kompassi at `localhost:8000`
2. Run this application `localhost:8001`
3. Try to log in

Expected results: You are logged in

Actual results: the login fails at `/oidc/callback/` because the session no longer has the OIDC state

Explanation: Both applications share the same set of cookies due to cookies being matched solely on the host name, not the port

Workaround: Add something like this to `/etc/hosts` and use `http://kompassi.dev:8000` and `http://infokala.dev:8001` instead.

    127.0.0.1 localhost kompassi.dev infokala.dev
