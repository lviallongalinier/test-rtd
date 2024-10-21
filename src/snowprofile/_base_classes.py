# -*- coding: utf-8 -*-

import datetime
import typing

import pydantic
import pydantic.json_schema
import numpy as np
import pandas as pd


class AdditionalData(pydantic.BaseModel):
    data: typing.Any


def force_utc(cls, value: datetime.datetime) -> datetime.datetime:
    """
    Force the tzinfo to be defined in a python datetime object.
    In case the tzinfo is not provided, assume UTC.
    """
    if value.tzinfo is None:
        return datetime.replace(tzinfo=datetime.timezone.utc)
    else:
        return value


datetime_with_tz = typing.Annotated[datetime.datetime, pydantic.BeforeValidator(force_utc)]


def force_utc_tuple(cls, value):
    """
    Same as force_utc but for all elements of a tuple.
    """
    for i in range(len(value)):
        value[i] = force_utc(value[i])


datetime_tuple_with_tz = typing.Annotated[typing.Tuple[typing.Optional[datetime.datetime],
                                                       typing.Optional[datetime.datetime]],
                                          pydantic.BeforeValidator(force_utc_tuple)]


class BaseProfile(pydantic.BaseModel):
    """
    Base class for all profiles (stratigraphy, density, etc.)
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid',
        arbitrary_types_allowed=True)

    id: typing.Optional[str] = pydantic.Field(
        None,
        description="Unique identifier of the profile [A-Za-z0-9-]")
    name: typing.Optional[str] = pydantic.Field(
        None,
        description="Name/short description of the profile")
    comment: typing.Optional[str] = pydantic.Field(
        None,
        description="A comment associated to the profile")
    record_time: typing.Optional[datetime_with_tz] = pydantic.Field(
        None,
        description="The time at which the profile observation have been done (python datetime object).")
    record_period: datetime_tuple_with_tz = pydantic.Field(
        (None, None),
        description="Time period of the profile observation "
        "(tuple of two python datetime object representing the begin time and end time).")
    profile_depth: typing.Optional[float] = pydantic.Field(
        None, ge=0,
        description="Profile depth if different from the SnowProfile one (m)")
    profile_swe: typing.Optional[float] = pydantic.Field(
        None, ge=0,
        description="Profile SWE if specific measurement at the precise location of the profile (mm or kg/m2)")
    additional_data: typing.Optional[AdditionalData] = pydantic.Field(
        None,
        description="Room to store additional data for CAAML compatibility (customData), do not use.")


class BaseProfileFields:
    """
    Base fields for all profiles except stratigraphy
    """
    data: typing.Annotated[pd.DataFrame, pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data (SI units)")
    quality_of_measurement: typing.Optional[typing.Literal[
        'Good', 'Uncertain', 'Low', 'Bad']] = pydantic.Field(
            None,
            description="Qualitative uncertainty of measurement compared to the reference uncertainty "
            "of the measurement method. Definitions: \n\n"
            ""
            "- Good: reliable data within the standard quality of the method\n"
            "- Uncertain: data whose quality is probably below the standard quality of the method "
            "(doubts in the measurement or data processing procedure). To be specified in the quality comment.\n"
            "- Low quality: data whose quality is undoubtedly below the standard quality of the method due to "
            "measurements or data processing procedure. To be specified in the quality comment.\n"
            "- Bad: undoubtedly erroneous data")
    uncertainty_of_measurement: typing.Optional[float] = pydantic.Field(
        None,
        description="Quantitative uncertainty on ``data``: standard deviation or 68% confidence interval. "
        "Same units as ``data``.")
    profile_nr: typing.Optional[int] = pydantic.Field(
        None, ge=0,
        description="Profile number (the lower is the higher priority)")


class BaseProfileLayered(BaseProfile):
    """
    Base class for layered profiles, including stratigraphy.
    """
    @property
    def bottom_depth(self) -> np.ndarray:
        """
        Get the bottom depth (numpy array, zero at ground)
        """
        return self.data['top_depth'].values - self.data['thicknesses'].values


class BaseProfileLayeredData(BaseProfileLayered, BaseProfileFields):
    """
    Base class for profiles with layer dimension (all except temperature)

    Data contain columns top_depth, thicknesses, data, comments, additonal_data.
    For depth, zero is at bottom of the snowpack.
    """

    # TODO: Implement a rewritting of arrays so that they are always presented in the same order  <18-10-24, LVG> #
    # TODO: Implement a method to insert a layer with top_depth, thicknesses, comments  <18-10-24, LVG> #
    # TODO: Implement check of data pandas dataframe  <18-10-24, Léo Viallon-Galinier> #


class BaseProfilePointData(BaseProfile, BaseProfileFields):
    """
    Base class for profiles measuring one data at a time (all except temeprature and stratigraphy)

    Data contain columns depth, data, comments, additonal_data.
    For depth, zero is at bottom of the snowpack.
    """
