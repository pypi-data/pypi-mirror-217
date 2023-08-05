.. image:: https://img.shields.io/pypi/v/flook.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/flook/
.. image:: https://github.com/norwik/flook/actions/workflows/ci.yml/badge.svg
    :alt: Build Status
    :target: https://github.com/norwik/flook/actions/workflows/ci.yml

|

======
Flook
======

A Lightweight and Flexible Ansible Command Line Tool.

To use flook, follow the following steps:

1. Create a python virtual environment or use system wide environment

.. code-block::

    $ python3 -m venv venv
    $ source venv/bin/activate


2. Install flook package with pip.

.. code-block::

    $ pip install flook


3. Get flook command line help

.. code-block::

    $ flook --help


4. Init the config file and the sqlite database

.. code-block::

    $ flook config init


5. To edit configs

.. code-block::

    $ flook config init


6. Add a recipe

.. code-block::

    $ flook recipe add <recipe_name> -p <recipe_relative_path>

    # Some examples
    $ flook recipe add clivern/ping -p recipe/ping -f
    $ flook recipe add clivern/nginx -p recipe/nginx -f
    $ flook recipe add clivern/motd -p recipe/motd -f


7. To list recipes

.. code-block::

    $ flook recipe list

    # Get recipes as a JSON
    $ flook recipe list -o json | jq .


8. To get a recipe

.. code-block::

    $ flook recipe get <recipe_name>


9. To delete a recipe

.. code-block::

    $ flook recipe delete <recipe_name>


10. Add a host

.. code-block::

    $ flook host add <host_name> -i <host_ip> -p <ssh_port> -u <ssh_username> -s <ssh_key_path>

    # Add a remote host
    $ flook host add example.com -i 127.0.0.1 -p 22 -u root -s /Users/root/.ssh/id_rsa.pem

    # Add the localhost
    $ flook host add localhost -i localhost -c local


11. To list hosts

.. code-block::

    $ flook host list

    # Get hosts as a JSON
    $ flook host list -o json | jq .


12. To get a host

.. code-block::

    $ flook host get <host_name>


13. To SSH into a host

.. code-block::

    $ flook host ssh <host_name>


14. To delete a host

.. code-block::

    $ flook host delete <host_name>


15. Run a recipe towards a host

.. code-block::

    $ flook recipe run <recipe_name> -h <host_name>

    # Some examples
    $ flook recipe run clivern/nginx -h example.com
    $ flook recipe run clivern/ping -h localhost
