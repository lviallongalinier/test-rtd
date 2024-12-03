Base classes for profiles per parameter
=======================================


Note that all the class below have a ``data`` property that contains the profile data.
It returns a pandas DataFrame for easy data processing. Note that the DataFrame should be reassignated to the ``data`` key so that the modifications are taken into account (a call to the ``data`` key return a copy of the internal data stored in the dataclass).

.. automodule:: snowprofile.profiles
   :members:
   :show-inheritance:
   :inherited-members: BaseModel
   :member-order: bysource
