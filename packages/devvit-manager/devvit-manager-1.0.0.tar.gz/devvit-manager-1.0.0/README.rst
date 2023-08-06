Devvit Manager: A Utility for Devvit Projects
=============================================

.. image:: https://img.shields.io/pypi/v/devvit-manager.svg
    :alt: Latest Devvit Manager Version
    :target: https://pypi.python.org/pypi/devvit-manager

.. image:: https://img.shields.io/pypi/pyversions/devvit-manager
    :alt: Supported Python Versions
    :target: https://pypi.python.org/pypi/devvit-manager

.. image:: https://img.shields.io/pypi/dm/devvit-manager
    :alt: PyPI - Downloads - Monthly
    :target: https://pypi.python.org/pypi/devvit-manager

.. image:: https://github.com/LilSpazJoekp/devvit-manager/workflows/CI/badge.svg
    :alt: GitHub Actions Status
    :target: https://github.com/LilSpazJoekp/devvit-manager/actions?query=branch%3Amaster

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :alt: pre-commit
    :target: https://github.com/pre-commit/pre-commit

.. image:: https://api.securityscorecards.dev/projects/github.com/LilSpazJoekp/devvit-manager/badge
    :alt: OpenSSF Scorecard
    :target: https://api.securityscorecards.dev/projects/github.com/LilSpazJoekp/devvit-manager

Devvit Manager is a Python package that enables you to easily utilize devvit with
multiple Reddit user accounts.

.. _installation:

Installation
------------

Devvit Manager is supported on Python 3.8+.

.. code-block:: bash

    pip install devvit-manager

To install the latest development version of Devvit Manager run the following instead:

.. code-block:: bash

    pip install --upgrade https://github.com/LilSpazJoekp/devvit-manager/archive/master.zip

Usage
-----

For a full list of commands and options run:

.. code-block:: bash

    devvit-mgr --help

To login a new user run:

.. code-block:: bash

    devvit-mgr login

To switch users run:

.. code-block:: bash

    devvit-mgr switch

To logout a user run:

.. code-block:: bash

    devvit-mgr remove

All commands except ``login`` can accept a single parameter for specifying a username
(case-sensitive). If one isn't provided, you will be prompted for one. All the commands
above can be run with the ``--help`` option to get more information.
