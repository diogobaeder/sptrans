Contributing
============

First of all, take a look at the repository `here <https://github.com/diogobaeder/sptrans>`_.

You may have noticed that there are two images in the README:
one that tells the status of the build (via Continuous Integration in `travis-ci <https://travis-ci.org/diogobaeder/sptrans>`_)
and another that tells the code coverage in `coveralls <https://coveralls.io/r/diogobaeder/sptrans>`_.

This is because I'm a bit obsessive with automated tests, and though I don't think 100% code coverage makes a program free of bugs,
it does a great job getting as close as possible to this achievement.

By the way, the build doesn't even pass if the production code is not fully covered, so if you want to contribute with it, please
also add some tests.

Setting up the environment
--------------------------

1. Make sure you have pip, virtualenv and virtualenvwrapper installed. OK, all of these are optional, but it would be a nice moment
   for you to start using them if you haven't yet;

2. Create a virtual environment for the project, and activate it;

3. Install the requirements for running the tests:

   .. code-block:: bash

    $ pip install -r requirements.txt

4. Run the tests:

   .. code-block:: bash

    $ tox

   Optionally, you can run the tests with an SPTrans API token, so that the functional tests are also run:

   .. code-block:: bash

    $ SPTRANS_TOKEN=this-is-my-token tox