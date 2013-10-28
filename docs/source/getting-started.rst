Getting started
===============

Before using the library, you need to have an API token issued at the SPTrans website.

As soon as you have the token, use the :class:`client <sptrans.v0.Client>` itself to authenticate to the API::

    from sptrans.v0 import Client


    client = Client()
    client.authenticate('this is my token')