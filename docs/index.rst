.. sptrans documentation master file, created by
   sphinx-quickstart on Mon Oct 28 04:21:33 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=======
sptrans
=======

Python library for the SPTrans API

.. toctree::
   :maxdepth: 4
   :hidden:

   /changelog
   /sptrans
   /contributing

About
=====

This library was developed as a Python client to the `SPTrans API <http://www.sptrans.com.br/desenvolvedores/APIOlhoVivo/Documentacao.aspx?1>`_.
It was made in English so that people from other countries can used it, and contribute to it, so you may expect some discrepancies between the library
and the SPTrans API itself.

Getting started
===============

Installing
----------

Plain and simple:

.. code-block:: bash

   $ pip install sptrans

Or, if you want the latest version under development:

.. code-block:: bash

   $ pip install -e git+https://github.com/diogobaeder/sptrans.git#egg=sptrans

Or, if you still don't want to use pip, just grab the code at GitHub and install it with:

.. code-block:: bash

   $ python setup.py install

Usage
-----

(:ref:`Looking for the library API? Here's a shortcut! <modindex>`)

Before using the library, you need to have an API token issued at the SPTrans website.

As soon as you have the token, use the :class:`client <sptrans.v0.Client>` itself to authenticate to the API::

    from sptrans.v0 import Client


    client = Client()
    client.authenticate('this is my token')

Now checkout the other methods available in the :class:`Client <sptrans.v0.Client>` class, to see how the library can help you retrieving data.

Documentation
=============

* :doc:`changelog`
* :doc:`library API <sptrans>`
* :doc:`contributing`

License
=======

Copyright (c) 2013, Diogo Baeder
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

  Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

