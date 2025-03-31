.. _io:

Reading and writting data
=========================

The ``SnowProfile`` object can be created by reading various data formats and can be saved in different formats. Functions to deals with input/output (i/o) of ``SnowProfile`` objects are gathered into the ``snowprofile.io`` module, which is documented below.

CAAML snowprofile format
^^^^^^^^^^^^^^^^^^^^^^^^

Reading and writting of the CAAML international format for exchange of snow profile observation data is possible by the snowprofile package with the two following functions:

.. autofunction:: snowprofile.io.read_caaml6_xml

.. autofunction:: snowprofile.io.write_caaml6_xml

Internal JSON representation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Temporary storage of the data in an internal JSON-based format. Note that this format is not intended to be used for persistant data storage. Re-read of such data may or may not be compatible between versions of the package.

.. autofunction:: snowprofile.io.read_internal_json

.. autofunction:: snowprofile.io.write_internal_json


You can also get access (and re-read) to an internal JSON-based representation with:

.. autofunction:: snowprofile.io.to_json

.. autofunction:: snowprofile.io.from_json

Dict-based representation
^^^^^^^^^^^^^^^^^^^^^^^^^

You can get a dict-based JSON-serializable representation of a ``SnowProfile`` object with:

.. autofunction:: snowprofile.io.to_dict


Reading profiles from csv files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: snowprofile.io.profile_csv.read_csv_profile

Meteo-France internal database (Bdclim)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Readers to get operational observations from Meteo-France internal database structure are available (writting in this format is not possible).

A function allows to identify available observations:

.. autofunction:: snowprofile.io.search_mf_bdclim_dates

A function allows to get the observation itself:

.. autofunction:: snowprofile.io.read_mf_bdclim

