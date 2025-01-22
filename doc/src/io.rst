Reading and writting data
=========================

The SnowProfile object (and only this one) can be stored into different formats and read from various formats. Functions to deals with I/O of SnowProfile objects are gathered into the ``snowprofile.io`` module which is documented below.

Internal JSON representation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Temporary storage of the data in an internal JSON-based format.

.. autofunction:: snowprofile.io.read_internal_json

.. autofunction:: snowprofile.io.write_internal_json


You can also get access (and re-read) to an internal JSON-based representation with:

.. autofunction:: snowprofile.io.to_json

.. autofunction:: snowprofile.io.from_json

Dict-based representation
^^^^^^^^^^^^^^^^^^^^^^^^^

You can get a dict-based JSON-serializable representation of a SnowProfile object with:

.. autofunction:: snowprofile.io.to_dict

