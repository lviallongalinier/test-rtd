Base classes for property profiles
==================================

This module gathers the classes to handle profile data. These classes are designed to be used in the :py:class:`~snowprofile.SnowProfile` class.

- :py:class:`~snowprofile.profiles.Stratigraphy`
- :py:class:`~snowprofile.profiles.TemperatureProfile`
- :py:class:`~snowprofile.profiles.DensityProfile`
- :py:class:`~snowprofile.profiles.LWCProfile`
- :py:class:`~snowprofile.profiles.SSAProfile`
- :py:class:`~snowprofile.profiles.SSAPointProfile`
- :py:class:`~snowprofile.profiles.HardnessProfile`
- :py:class:`~snowprofile.profiles.HardnessPointProfile`
- :py:class:`~snowprofile.profiles.StrengthProfile`
- :py:class:`~snowprofile.profiles.ImpurityProfile`
- :py:class:`~snowprofile.profiles.ScalarProfile`
- :py:class:`~snowprofile.profiles.VectorialProfile`

**All the class above have a** ``data`` **key that contains the profile data, stored as a pandas DataFrame.**

Note: when the dataframe is modified, the dataframe needs to be  reassignated to the ``data`` key so that the modifications are taken into account (a call to the ``data`` key returns a copy of the internal data stored in the dataclass).

.. automodule:: snowprofile.profiles
   :members:
   :show-inheritance:
   :inherited-members: BaseModel
   :member-order: bysource
