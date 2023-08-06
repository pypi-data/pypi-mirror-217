**********
idem-posix
**********

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-idem-teal
   :alt: Made with idem, a Python implementation of Plugin Oriented Programming
   :target: https://www.idemproject.io/

.. image:: https://img.shields.io/badge/docs%20on-docs.idemproject.io-blue
   :alt: Documentation is published with Sphinx on docs.idemproject.io
   :target: https://docs.idemproject.io/idem-aws/en/latest/index.html

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

**Grains, execution modules, and state modules common to all posix systems**

About
=====

``idem-posix`` helps executing commands on a posix system ``idem``.

* `idem-posix source code <https://gitlab.com/vmware/idem/idem-posix>`__
* `idem-posix documentation <https://docs.idemproject.io/idem-posix/en/latest/index.html>`__

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

What is Idem?
-------------

This project is built with `idem <https://www.idemproject.io/>`__, an idempotent,
imperatively executed, declarative programming language written in Python. This project extends
idem!

For more information:

* `Idem Project Website <https://www.idemproject.io/>`__
* `Idem Project docs portal <https://docs.idemproject.io/>`__


Installation
============

Install with pip::

    pip install idem-posix

Development Installation
========================

Clone the `idem-posix` repo and install with pip::

    git clone https://gitlab.com/vmware/idem/idem-posix idem_posix
    pip install -e idem_posix

Execution
=========
After installation the Idem Posix Provider execution and state modules will be accessible to the pop ``hub``.
In order to use them we need to set up our credentials.

Example of using cmd.run state in SLS:

.. code-block:: sls

    # Execute "ls -l" command
    my_state_name:
      cmd.run:
        cmd: ls -l
        cwd: /
        shell: False
        env:
          ENV_VAR_1: ENV_VAL_1
          ENV_VAR_2: ENV_VAL_2
        timeout: 100
        render_pipe:
        kwargs:

Example of using cmd.run with Idem CLI:

.. code-block:: bash

    idem exec cmd.run "shell command --with-flags" cwd=/home render_pipe=json timeout=10
