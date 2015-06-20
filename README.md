# Tracon's deployment of [Infokala]

This is a [Kompassi]-integrated deployment of [Infokala] that authenticates users from Kompassi via OAuth2 and gets event info from Kompassi using the public API of Kompassi.

[Infokala]: https://github.com/kcsry/infokala "Infokala, the Info Log Management System for Tracon & Desucon"
[Kompassi]: https://github.com/tracon/kompassi "Kompassi, the Tracon Event Management System"

## [Infokala] is installed using `pip`

Note that this repository does not contain the actual source code for the [Infokala] application. The actual application consists of the package called `infokala` that is installed using `pip` from `requirements.txt`. The version of Infokala to use is selected in `requirements.txt`.

This repository is responsible for setting up the Tracon/Kompassi specific bits for Infokala, such as the Kompassi OAuth2 based authentication and group membership based authorization.

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

    source venv-kompassi/bin/activate
    git clone https://github.com/tracon/infokala-tracon.git
    cd infokala-tracon
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py infokala_setup_basic_workflow traconx
    ./manage.py runserver 127.0.0.1:8001
    iexplore http://infokala.dev:8001/events/traconx/messages/

## Authentication and authorization

Authentication is performed via OAuth2 against Kompassi. All users that are present in Kompassi are allowed to log in.

Authorization is performed using group membership information extracted from the Kompassi `/api/v2/people/me` endpoint. Groups that grant access to different events' info logs are configurable. The admin group by default grants access to all events.

By default, these are configured as follows:

    INFOKALA_ACCESS_GROUP_TEMPLATES = [
        '{kompassi_installation_slug}-{event_slug}-labour-conitea',
        '{kompassi_installation_slug}-{event_slug}-labour-info',
    ]

    KOMPASSI_INSTALLATION_SLUG = 'turska'
    KOMPASSI_ADMIN_GROUP = 'admins'

That would basically grant access to the organizing committee (*conitea*) and info workers.

## Development gotchas

### "OAuth2 MUST use HTTPS"

Technically it's horribly wrong to use OAuth2 over insecure HTTP. However, it's tedious to set up TLS for development. That's why we monkey patch `oauthlib.oauth2:is_secure_transport` on `DEBUG = True`. See `infokala_tracon/settings.py`.

### Applications on `localhost` in different ports share the same cookies

1. Run Kompassi at `localhost:8000`
2. Run this application `localhost:8001`
3. Try to log in

Expected results: You are logged in

Actual results: 500 Internal Server Error due to session not having `oauth_state` in `/oauth2/callback`

Explanation: Both applications share the same set of cookies due to cookies being matched solely on the host name, not the port

Workaround: Add something like this to `/etc/hosts` and use `http://kompassi.dev:8000` and `http://infokala.dev:8001` instead.

    127.0.0.1 localhost kompassi.dev infokala.dev
