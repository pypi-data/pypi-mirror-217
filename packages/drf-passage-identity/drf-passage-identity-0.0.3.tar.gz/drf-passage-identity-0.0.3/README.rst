=====================
drf-passage-identity
=====================

A Django App that allows you to easilty integrate Passwordless authentication provided by Passage (by 1Password). Leverage a custom PassageUser module over the User module provided by Django but with built-in Passage user integration and token authentication for seamless passwordless authentication via REST APIs.

----

Setup
-----

Install from **pip**:

.. code-block:: sh

    python -m pip install drf-passage-identity

and then add it to your installed apps:

.. code-block:: python

    INSTALLED_APPS = [
        ...,
        "passage_auth",
        ...,
    ]

Make sure you add the trailing comma or you might get a ``ModuleNotFoundError``
(see `this blog
post <https://adamj.eu/tech/2020/06/29/why-does-python-raise-modulenotfounderror-when-modifying-installed-apps/>`__).

You will also need to add a path to listen in get responses:

.. code-block:: python

    urlpatterns = [
        ...,
        path('api/client/', include("passage_auth.urls")),
        ...,
    ]



Configuration
-------------

Configure the Passage object in your Django settings. Here, for Header Auth, auth strategy is 2 and for Cookie Auth it is 1. You must set the following settings:

.. code-block:: python

    AUTH_USER_MODEL = 'passage_auth.PassageUser'
    PASSAGE_APP_ID = "your-app-id"
    PASSAGE_API_KEY = "your-api-key"
    PASSAGE_AUTH_STRATEGY = 2




