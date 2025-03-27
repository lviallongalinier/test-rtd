.. _Install:

Install
=======

We recommend to install the package in a virtual environment.

Creating a virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are used to a method to create virtual environment, just use the metod you are used to. Otherwise, python is shipped with the ``venv`` tool:


1. Create a virtual environment by running ``python3 -m venv <virtual_environment_name>``
2. Enter the environment by running ``source <virtual_environment_name>/bin/activate``.

To quit the virtual environment, use the ``deactivate`` command.

Install for users
^^^^^^^^^^^^^^^^^

Users can install the ``snowprofile`` package with pip :

.. code-block:: bash

   pip install snowprofile

Install for developpers
^^^^^^^^^^^^^^^^^^^^^^^

Developers should first clone the git repository:

.. code-block:: bash

   git clone git@github.com:UMR-CNRM/snowprofile.git

Then, install in your virtual environment in editable mode:

.. code-block:: bash

   pip install -e <path/to/the/git/repository/of/snowprofile>

This way, changes done to the git repository will be available immediately in the virtual environment (after restarting python if used interactively).
