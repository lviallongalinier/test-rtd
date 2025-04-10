snowprofile's |version| documentation
=====================================

Documentation of snowprofile |version| generated on |today|.

Presentation
------------

The snowprofile python package allows to handle a dataset of vertical profiles of snow properties, such as stratigraphy, density or SSA profiles. The package is based on the creation and manipulation of :py:class:`snowprofile.snowprofile.SnowProfile` python objects.
A ``SnowProfile`` object contains profiles that share the same location and time.

The snowprofile package allows to:

- read existing profile data in various formats, notably CSV and CAAML snow profile (see :ref:`io`), or enter new profile data via python code. Data read in or entered manually is stored in a python object architecture :py:class:`snowprofile.snowprofile.SnowProfile`

- merge files of different profile into a single file of profiles (:py:func:`snowprofile.SnowProfile.merge`)

- save a set of profiles in CAAML snow profile formats (see :ref:`io`)
 
- vizualize the profiles of snow properties with basic plotting tools (matplotlib)



Get started
-----------

.. toctree::
   :maxdepth: 1

   plot.rst
   read_write.rst
   comments.rst
   uncertainties.rst
   units.rst
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
