# -*- coding: utf-8 -*-

import typing

import pydantic

from snowprofile.classes import Time, Observer, Location, Weather, SurfaceConditions, Environment
from snowprofile.profiles import Stratigraphy, TemperatureProfile, DensityProfile, LWCProfile, _SSAProfile, \
    _HardnessProfile, StrengthProfile, ImpurityProfile, ScalarProfile, VectorialProfile
from snowprofile.stability_tests import _StabilityTest
from snowprofile._base_classes import AdditionalData


class SnowProfile(pydantic.BaseModel):

    """
    The base class for representing and manipulating a snow profile.

    Data content
    ^^^^^^^^^^^^

    General information on snow profile and snow pit
    ''''''''''''''''''''''''''''''''''''''''''''''''

    id
      A unique id to identify the snow profile (optional, str, only [a-zA-Z0-9-])

    comment
      General comment on the overall measurement (optional, str)

    profile_comment
      General comment on the snow profile (optional, str)

    time
      Time of observation (Time object)

    observer
      Observer information (Observer object)

    location
      Location information (Location object)

    weather
      Weather observations (Weather object)

    surface_conditions
      Surface conditions (penetration depths, surface features, wind surface features, etc.) (SurfaceConditions object)

    profile_depth
      Depth of the profile (m)

    profile_depth_std
      Standard deviation of the profile depth around the snow pit in case of multiple measurements (m)

    profile_swe
      Measured total SWE (mm or kg/m2)

    profile_swe_std
      Standard deviation of the measured SWE (in case of mutilple measurements, mm or kg/m2)

    new_snow_24_depth
      Depth of the sen snow (past 24h) (m)

    new_snow_24_depth_std
      Standard deviation of the depth of new snow in case of multiple measurements (m)

    new_snow_24_swe
      Measured total new snow SWE (24h) (mm or kg/m2)

    new_snow_24_swe_std
      Standard deviation of the measured new snow SWE (in case of mutilple measurements, mm or kg/m2)

    snow_transport
      Presence and type of snow transport

      - No snow transport
      - Modified saltation: snow transport that remains confined close to the ground
      - Drifting snow: transport up to 6ft/2m
      - Blowing snow: transport above 6ft/2m

    snow_transport_occurence_24: typing.Optional[float] = pydantic.Field(None, ge=0, le=100)

    Profiles data
    '''''''''''''

    stratigraphy_profile
      The stratigraphy profile (unique, StratigraphyProfile object)

    temperature_profiles:
      Temperature profiles (list of TemperatureProfile objects)

    density_profiles:
      Density profiles (list of DensityProfile objects)

    lwc_profiles:
      LWC profiles (list of LWCProfile objects)

    ssa_profiles:
      SSA profiles (list of SSAProfile objects)

    hardness_profiles:
      Hardness profiles (list of HardnessProfile objects)

    strength_profiles:
      Strength profiles (list of StrengthProfile objects)

    impurity_profiles:
      Impurity profiles (list of ImpurityProfile objects)

    stability_tests: typing.List[StabilityTest]  # To change: accept different stability tests

    Other data
    ''''''''''

    application
      Information on the application that generated the profile (optional, str)

    application_version
      Version of the application that generated the profile (optional, str)

    profiles_comment
      Comment associated to profiles, for CAAML compatibility only, do not use (str)

    additional_data and profiles_additional_data
      Room to store additional data for CAAML compatibility (customData), do not use.

    """

    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    id: typing.Optional[str] = None
    comment: typing.Optional[str] = None
    profile_comment: typing.Optional[str] = None
    profiles_comment: typing.Optional[str] = None
    time: Time = Time()
    observer: Observer = Observer()
    location: Location = Location(name='Unknown', latitude=43.600824, longitude=1.432964)
    environment: Environment = Environment()
    application: typing.Optional[str] = 'snowprofile'
    application_version: typing.Optional[str] = None
    profile_depth: typing.Optional[float] = pydantic.Field(None, ge=0)
    profile_depth_std: typing.Optional[float] = pydantic.Field(None, ge=0)
    profile_swe: typing.Optional[float] = pydantic.Field(None, ge=0)
    profile_swe_std: typing.Optional[float] = pydantic.Field(None, ge=0)
    new_snow_24_depth: typing.Optional[float] = pydantic.Field(None, ge=0)
    new_snow_24_depth_std: typing.Optional[float] = pydantic.Field(None, ge=0)
    new_snow_24_swe: typing.Optional[float] = pydantic.Field(None, ge=0)
    new_snow_24_swe_std: typing.Optional[float] = pydantic.Field(None, ge=0)
    snow_transport: typing.Optional[typing.Literal[
        'No snow transport',
        'Modified saltation',
        'Drifting snow',
        'Blowing snow']] = None
    snow_transport_occurence_24: typing.Optional[float] = pydantic.Field(None, ge=0, le=100)
    weather: Weather = Weather()
    surface_conditions: SurfaceConditions = SurfaceConditions()
    stratigraphy_profile: typing.Optional[Stratigraphy] = None
    temperature_profiles: typing.List[TemperatureProfile] = []
    density_profiles: typing.List[DensityProfile] = []
    lwc_profiles: typing.List[LWCProfile] = []
    ssa_profiles: typing.List[_SSAProfile] = []
    hardness_profiles: typing.List[_HardnessProfile] = []
    strength_profiles: typing.List[StrengthProfile] = []
    impurity_profiles: typing.List[ImpurityProfile] = []
    other_scalar_profiles: typing.List[ScalarProfile] = []
    other_vectorial_profiles: typing.List[VectorialProfile] = []
    stability_tests: typing.List[_StabilityTest] = []  # To change: accept different stability tests
    additional_data: typing.Optional[AdditionalData] = None
    profiles_additional_data: typing.Optional[AdditionalData] = None
