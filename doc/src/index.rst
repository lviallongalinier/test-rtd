snowprofile's |version| documentation
=====================================

Documentation of snowprofile |version| generated on |today|.

Presentation
------------

The snowprofile python package allows to handle a dataset of vertical profiles of snow properties, such as stratigraphy, density or SSA profiles. The package is based on the creation and manipulation of :py:class:`~snowprofile.snowprofile.SnowProfile` python objects.
A ``SnowProfile`` object contains profiles that share the same location and time.

The snowprofile package allows to:

- read existing profile data in various formats, notably CSV and CAAML snow profile (see :ref:`io`), or enter new profile data via python code. Data read in or entered manually is stored in a python object architecture :py:class:`~snowprofile.snowprofile.SnowProfile`.
- merge files of different profile into a single file of profiles (see :py:func:`snowprofile.SnowProfile.merge`)
- read/save a set of profiles from/to CAAML snow profile formats (see :ref:`io`)
- convert observed snow profiles between different formats (as a consequence of previous point)
- vizualize the profiles of snow properties with basic plotting tools (matplotlib)


For the installation, see:

.. toctree::
   :maxdepth: 1

   install.rst


Get started: Concepts to understand before using the package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You will manipulate :py:class:`~snowprofile.snowprofile.SnowProfile` objects mainly. Heve a llok to the corresponding documentation

To get started, you can start with reading these first points:

.. toctree::
   :maxdepth: 1

   read_write.rst
   overview.rst
   units.rst

For more advances use cases, please also consider the additional concepts:

.. toctree::
   :maxdepth: 1

   comments.rst
   uncertainties.rst
   configuration.rst

Description of the data classes
-------------------------------

.. toctree::
   :maxdepth: 1

   snowprofile.rst

The ``SnowProfile`` object relies on additional classes:

.. toctree::
   :maxdepth: 1

   classes.rst
   profiles.rst
   stability_tests.rst

I/O reading and writting data
-----------------------------

.. toctree::
   :maxdepth: 2

   io.rst

Documentation for developers
----------------------------

.. toctree::
   :maxdepth: 1

   develop.rst


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
