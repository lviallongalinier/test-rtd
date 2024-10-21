# -*- coding: utf-8 -*-

import typing
import datetime

import pydantic

from snowprofile._constants import cloudiness_attribution
from snowprofile._base_classes import AdditionalData, datetime_with_tz, datetime_tuple_with_tz


class Time(pydantic.BaseModel):
    """
    Class to store the date and time of observation (and additional date/time considerations)

    Be carfeul: If the python datetime object does not have time zone, the time zone will be
    automatically filled and the time zone is assumed to be UTC.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    record_time: datetime_with_tz = pydantic.Field(
        datetime.datetime.now(),
        description="The time at which the observation have been done (python datetime object).")
    record_period: datetime_tuple_with_tz = pydantic.Field(
        (None, None),
        description="Time period of the observation "
        "(tuple of two python datetime object representing the begin time and end time).")
    report_time: datetime_with_tz = pydantic.Field(
        None,
        description="Reporting time of the observation (python datetime object).")
    last_edition_time: datetime_with_tz = pydantic.Field(
        None,
        description="Last edition time of this observation data (python datetime object).")
    comment: typing.Optional[str] = pydantic.Field(
        None,
        description="Comment on observation date/time (str)")
    additional_data: typing.Optional[AdditionalData] = pydantic.Field(
        None,
        description="Room to store additional data for CAAML compatibility (customData), do not use.")


class Observer(pydantic.BaseModel):
    """
    Class to store observation institution and observer details.

    ``source`` refer to the observation institution and ``person`` to the
    observer. Both can be filled or only one of the two.

    Data content
    ^^^^^^^^^^^^

    source_id
      Unique identifier of the observation institution

    source_name
      Name of the observation institution

    source_comment
      Comment on the observation institution

    person_id
      Unique identifier of the observer

    person_name
      Name of the observer

    person_comment
      Comment on the observer

    source_additional_data and person_additional_data
      Room to store additional data for CAAML compatibility (customData), do not use.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    source_id: typing.Optional[str] = None
    source_name: typing.Optional[str] = None
    source_comment: typing.Optional[str] = None
    source_additional_data: typing.Optional[AdditionalData] = None

    person_id: typing.Optional[str] = None
    person_name: typing.Optional[str] = None
    person_comment: typing.Optional[str] = None
    person_additional_data: typing.Optional[AdditionalData] = None


class Location(pydantic.BaseModel):
    """
    Class to store the observation location details (geographical position).

    The required data fields are ``name``, ``latitude`` and ``longitude``.

    Data content
    ^^^^^^^^^^^^

    id
      A unique identifier for the goeographical point

    name
      The name of the observation location (str)

    latitude
      Latitude (degrees north)

    longitude
      Longitude (degrees East)

    comment
      A comment for the point descritpion (str)

    elevation
      Point elevation (meters above sea level)

    aspect
      Slope aspect (degrees, int between 0 and 360)

    slope
      Slope inclination (degrees, int between 0 and 90)

    point_type
      A point type description (str)

    country
      Country code according to ISO3166

    region
      Region (detail in the country, optional, str)

    additonal_data:
      Room to store additional data for CAAML compatibility (customData), do not use.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    id: typing.Optional[str] = None
    name: str
    point_type: typing.Optional[str] = None
    aspect: typing.Optional[int] = pydantic.Field(None, ge=0, le=360)
    elevation: typing.Optional[int] = None
    slope: typing.Optional[int] = pydantic.Field(None, ge=0, lt=90)
    latitude: float
    longitude: float
    country: typing.Optional[typing.Literal[
        "AD", "AE", "AF", "AG", "AL", "AM", "AO", "AR", "AT", "AU",
        "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ",
        "BN", "BO", "BQ", "BR", "BS", "BT", "BW", "BY", "BZ", "CA",
        "CD", "CF", "CG", "CH", "CI", "CL", "CM", "CN", "CO", "CR",
        "CU", "CV", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ",
        "EC", "EE", "EG", "ER", "ES", "ET", "FI", "FJ", "FM", "FR",
        "GA", "GB", "GD", "GE", "GH", "GL", "GM", "GN", "GQ", "GR",
        "GT", "GW", "GY", "HN", "HR", "HT", "HU", "ID", "IE", "IL",
        "IN", "IQ", "IR", "IS", "IT", "JM", "JO", "JP", "KE", "KG",
        "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KZ", "LA", "LB",
        "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA",
        "MC", "MD", "ME", "MG", "MH", "MK", "ML", "MM", "MN", "MR",
        "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NE", "NG",
        "NI", "NL", "NO", "NP", "NR", "NZ", "OM", "PA", "PE", "PG",
        "PH", "PK", "PL", "PS", "PT", "PW", "PY", "QA", "RO", "RS",
        "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI",
        "SK", "SL", "SM", "SN", "SO", "SR", "SS", "ST", "SV", "SY",
        "SZ", "TD", "TG", "TH", "TJ", "TL", "TM", "TN", "TO", "TR",
        "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ",
        "VC", "VE", "VN", "VU", "WF", "WS", "YE", "ZA", "ZM", "ZW"]] = None  # ISO 3166
    region: typing.Optional[str] = None
    comment: typing.Optional[str] = None
    additional_data: typing.Optional[AdditionalData] = None

    @pydantic.field_validator('country', mode='before')
    def _preprocess_country(country: typing.Optional[str]) -> typing.Optional[str]:
        """
        Ensure country code is upper case
        """
        if country is not None:
            return country.upper()
        return None


class Weather(pydantic.BaseModel):
    """
    Class to store the weather at timeof observation.

    Data content
    ^^^^^^^^^^^^

    cloudiness
      The cloudiness in the form of METAR code (CLR, FEW, SCT, BKN, OVC, X)
      or cloudiness in octas (from 0 to 8).

    precipitation
      Precipitation type at the time of observation, METAR code:

      - DZ: Drizzle
      - RA: Rain
      - SN: Snow (snow flakes)
      - SG: Snow grains
      - IC: Ice crystals
      - PE: ??
      - GR: Hail (Grèle)
      - GS: Graupel (Grésil)

      All these precipitation types could be preceded with '-' for light intensity or '+' for heavy intensity.
      The qualifier without +/- is moderate intensity.

      - UP: Unknown precipitation type
      - RASN: Rain and snow
      - FZRA: Frezzing rain
      - Nil in case of no precipitations

    air_temperature
      Temperature of air (°C)

    wind_speed
      Wind speed (m/s)

    wind_direction
      Wind direction (in degree, from 0 to 360)

    air_temperature_measurement_height
      Height for the air temperature measurement (m)

    wind_measurement_height
      Height for the wind speed and direction measurement (m)

    additonal_data:
      Room to store additional data for CAAML compatibility (customData), do not use.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    cloudiness: typing.Optional[typing.Literal[
        'CLR', 'FEW', 'SCT', 'BKN', 'OVC', 'X']] = None
    precipitation: typing.Optional[typing.Literal[
        "-DZ", "DZ", "+DZ", "-RA", "RA", "+RA", "-SN", "SN", "+SN",
        "-SG", "SG", "+SG", "-IC", "IC", "+IC", "-PE", "PE", "+PE",
        "-GR", "GR", "+GR", "-GS", "GS", "+GS"
        "UP", "Nil", "RASN", "FZRA"]] = None
    air_temperature: typing.Optional[float] = None
    wind_speed: typing.Optional[float] = pydantic.Field(None, ge=0)
    wind_direction: typing.Optional[int] = pydantic.Field(None, ge=0, le=360)
    air_temperature_measurement_height: typing.Optional[float] = pydantic.Field(None, gt=0)
    wind_measurement_height: typing.Optional[float] = pydantic.Field(None, gt=0)
    comment: typing.Optional[str] = None
    additional_data: typing.Optional[AdditionalData] = None

    @pydantic.field_validator('cloudiness', mode='before')
    def _preprocess_cloudiness(cloudiness: typing.Optional[str | int]) -> typing.Optional[str]:
        """
        Ensure cloudiness is upper case and convert octas to METAR code
        """
        if cloudiness is not None:
            if isinstance(cloudiness, str):
                return cloudiness.upper()
            elif isinstance(cloudiness, int):
                if cloudiness in cloudiness_attribution:
                    return cloudiness_attribution[cloudiness]
            return cloudiness
        return None


class SpectralAlbedo(pydantic.BaseModel):
    """
    Class to store spectral albedo
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid',
        arbitrary_types_allowed=True)

    comment: typing.Optional[str] = None
    # TODO: tbd  <17-10-24, Léo Viallon-Galinier> #


class SurfaceConditions(pydantic.BaseModel):
    """
    Description of the snow surface conditions.

    Data content
    ^^^^^^^^^^^^

    surface_roughness
      Surface roughness according to Fierz et al., 2009:

      - rsm: smooth
      - rwa: wavy (ripples)
      - rcv: concave furrows (ablation hollows, sun cups, penitents, due to melt or sublimation)
      - rcx: conex furrows (rain or melt groves)
      - rrd: random furrows (due to wind erosion)

    surface_wind_features
      Wind features observable at surface:

      - No observable wind bedforms
      - Snowdrift around obstacles
      - Snow ripples
      - Snow waves
      - Barchan dunes
      - Dunes
      - Loose patches
      - Pits
      - Snow steps
      - Sastrugi
      - mixed
      - other

    surface_other_features
      Other surface features among:

      - Sun cups
      - Penitents
      - Melt or rain furrows
      - other

    surface_features_amplitude
      Amplitude of surface features (m)

    surface_features_wavelength
      Wavelength of surface features (m)

    surface_features_aspect
      Orientation of surface features (degree, from 0 to 360)

    lap_presence
      Indication of the presence of light absorbing particule at the surface of snow. Values among:

      - No LAP
      - Black Carbon
      - Dust
      - Mixed
      - other

    surface_temperature
      Surface temperature (°C)

    surface_temperature_measurement_method
      Measurement method for the surface temperature among:

      - Thermometer
      - Hemispheric IR
      - IR thermometer
      - other

    additonal_data:
      Room to store additional data for CAAML compatibility (customData), do not use.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    surface_roughness: typing.Optional[typing.Literal[
        'rsm', 'rwa', 'rcv', 'rcx', 'rrd']] = None
    surface_wind_features: typing.Optional[typing.Literal[
        "No observable wind bedforms",
        "Snowdrift around obstacles",
        "Snow ripples",
        "Snow waves",
        "Barchan dunes",
        "Dunes",
        "Loose patches",
        "Pits",
        "Snow steps",
        "Sastrugi",
        "mixed",
        "other"]] = None
    surface_other_features: typing.Optional[typing.Literal[
        "Sun cups",
        "Penitents",
        "Melt or rain furrows",
        "other"]] = None
    surface_features_amplitude: typing.Optional[float] = pydantic.Field(None, gt=0)
    surface_features_wavelength: typing.Optional[float] = pydantic.Field(None, gt=0)
    surface_features_aspect: typing.Optional[int] = pydantic.Field(None, ge=0, le=360)
    lap_presence: typing.Optional[typing.Literal[
        "No LAP", "Black Carbon", "Dust",
        "Mixed", "other"]] = None
    surface_temperature: typing.Optional[float] = None
    surface_temperature_measurement_method: typing.Optional[typing.Literal[
        'Thermometer', 'Hemispheric IR', 'IR thermometer', 'other']] = None
    surface_albedo: typing.Optional[float] = None
    surface_albedo_comment: typing.Optional[str] = None
    spectral_albedo: typing.List[SpectralAlbedo] = []
    penetration_ram: typing.Optional[float] = pydantic.Field(None, ge=0)
    penetration_foot: typing.Optional[float] = pydantic.Field(None, ge=0)
    penetration_ski: typing.Optional[float] = pydantic.Field(None, ge=0)
    comment: typing.Optional[str] = None
    additional_data: typing.Optional[AdditionalData] = None
