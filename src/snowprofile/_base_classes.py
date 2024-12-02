# -*- coding: utf-8 -*-

"""
Base Classes and field validators that are used in the snowprofile, classes, profiles
stability_tests packages.
"""

import datetime
import typing
import logging

import pydantic
import pydantic.json_schema
import pandas as pd


class AdditionalData(pydantic.BaseModel):
    data: typing.Any


def force_utc(value: datetime.datetime) -> datetime.datetime:
    """
    Force the tzinfo to be defined in a python datetime object.
    In case the tzinfo is not provided, assume UTC.
    """
    if value.tzinfo is None:
        return value.replace(tzinfo=datetime.timezone.utc)
    else:
        return value


datetime_with_tz = typing.Annotated[datetime.datetime, pydantic.BeforeValidator(force_utc)]


def force_utc_tuple(value: tuple) -> tuple:
    """
    Same as force_utc but for all elements of a tuple.
    """
    for i in range(len(value)):
        value[i] = force_utc(value[i])
    return value


datetime_tuple_with_tz = typing.Annotated[typing.Tuple[typing.Optional[datetime.datetime],
                                                       typing.Optional[datetime.datetime]],
                                          pydantic.BeforeValidator(force_utc_tuple)]


def get_dataframe_checker(_mode='Layer', **kwargs):
    """
    Checker for pandas DataFrame to be put in a ``data`` field.

    :param _mode: Point or Layer or Spectral
    :param kwargs: dict:
        keys : list of columns ot be accepted
        values : dict with constraints on the content of the columns, keys are:
            - translate: dict of replacement for values.
            - type: data type (float, int, str, etc.)
            - optional (bool): Optional or not (default is False)
            - min: for numeric types, the minimum value possible (included)
            - max: for numeric types, the maximim value possible (included)
            - nan_allowed: for numeric types, allow nan or not (default is False)
            - values: the list of accepted values
    """
    def check_dataframe(value, cls=None):
        # Check type -> ensure we have a pandas DataFrame
        if isinstance(value, dict):
            value = pd.DataFrame(value)
        elif isinstance(value, pd.DataFrame):
            value = value.copy()
        else:
            raise ValueError('data key should be a pandas DataFrame or a python dictionnary.')

        # Check columns
        columns = set(value.columns)
        if _mode == 'Layer':
            two_of_three = set(['top_depth', 'bottom_depth', 'thickness'])
            if len(columns.intersection(two_of_three)) != 2:
                raise ValueError(f'Should have 2 of three in {", ".join(two_of_three)}.')
            accepted_columns_min = set([])
            accepted_columns_max = set(['top_depth', 'bottom_depth', 'thickness'])
        elif _mode == "Spectral":
            accepted_columns_min = set(['min_wavelength', 'max_wavelength'])
            accepted_columns_max = accepted_columns_min
        elif _mode == 'Point':
            accepted_columns_min = set(['depth'])
            accepted_columns_max = set(['depth'])
        elif _mode == 'None':
            accepted_columns_min = set()
            accepted_columns_max = set()
        else:
            raise ValueError(f'Mode {_mode} unknown. The data model is ill-defined.')

        columns_min = []
        for k, v in kwargs.items():
            if 'optional' in v and v['optional']:
                continue
            else:
                columns_min.append(k)
        columns_min = set(columns_min) | accepted_columns_min
        columns_max = set(kwargs.keys()) | accepted_columns_max
        if not columns.issuperset(columns_min):
            raise ValueError(f'The data should contain at least the following columns: {", ".join(columns_min)}.')
        if not columns.issubset(columns_max):
            raise ValueError(f'The data should contain at most the following columns: {", ".join(columns_max)}.')

        # Depths processing
        # - Ensure types
        if _mode == 'Layer':
            depth_keys = ['top_depth', 'bottom_depth', 'thickness']
        elif _mode == "Point":
            depth_keys = ['depth']
        elif _mode == "Spectral":
            depth_keys = ['min_wavelength', 'max_wavelength']
        else:
            depth_keys = []
        for key in depth_keys:
            if key in columns:
                value[key] = value[key].astype('float')
        # - Completion of columns to ensure that top_depth, bottom_depth an dthickess are defined and coherent
        if _mode == 'Layer':
            if 'top_depth' not in columns:
                value['top_depth'] = value['bottom_depth'] + value['thickness']
            if 'bottom_depth' not in columns:
                value['bottom_depth'] = value['top_depth'] - value['thickness']
            if 'thickness' not in columns:
                value['thickness'] = value['top_depth'] - value['bottom_depth']
        # - Ensure reasonnable values and no nan
        for key in depth_keys:
            if pd.isna(value[key]).any():
                raise ValueError(f'Nan values are not allowed in {key} field')
            if value[key].min() < 0:
                raise ValueError(f'Negative values for {key} is not accepted.')
            if _mode in ['Point', 'Layer'] and value[key].max() > 10:
                logging.warn(f'Values above 10m for {key}. Please check your data !')

        # Check other data
        for key, d in kwargs.items():
            if key not in value.columns:
                continue
            # Replace values if needed
            if 'translate' in d:
                value[key] = value[key].replace(d['translate'])
            # Check type
            _type = d['type'] if 'type' in d else 'float'
            value[key] = value[key].astype(_type)
            # Check min/max for numeric types
            if pd.isna(value[key].min()):
                logging.warn(f'Data from key {key} is empty !')
            if 'min' in d:
                _min = d['min']
                if not pd.isna(value[key].min()) and value[key].min() < _min:
                    raise ValueError(f'Data from key {key} has unaccepted values (below {_min}).')
            if 'max' in d:
                _max = d['max']
                if not pd.isna(value[key].max()) and value[key].max() > _max:
                    raise ValueError(f'Data from key {key} has unaccepted values (above {_max}).')
            # Check nan presence
            nan_allowed = d['nan_allowed'] if 'nan_allowed' in d else False
            if not nan_allowed and pd.isna(value[key]).any():
                raise ValueError(f'Nan values are not allowed in {key} field')
            # Check fixed allowed values if needed
            if 'values' in d:
                if not set(value[key].values).issubset(set(d['values'])):
                    raise ValueError(f'Unauthorized value for key {key}')

        return value.sort_values(depth_keys[0], ascending=False)

    return check_dataframe


class BaseProfile(pydantic.BaseModel):
    """
    Base class used for all profiles (stratigraphy, density, etc.)

    See the child class BaseProfile2 for all profiles except stratigraphy.
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
    related_profiles: typing.List[str] = pydantic.Field(
        [],
        description="id of related profiles"),
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
    _data = typing.Optional[pd.DataFrame]

    def __init__(self, data=None, data_dict=None, **kwargs):
        super().__init__(**kwargs)
        checker = get_dataframe_checker(**self._data_config)
        if data is not None:
            self._data = checker(data)
        elif data_dict is not None:
            self._data = checker(data_dict)
        else:
            raise ValueError('data key is required')

    @property
    def data(self) -> pd.DataFrame:
        """
        The profile data in the form of a Pandas Dataframe
        """
        if self._data is not None:
            return self._data.copy()
        else:
            return None

    @data.setter
    def data(self, value):
        checker = get_dataframe_checker(**self._data_config)
        self._data = checker(value)

    @data.deleter
    def data(self):
        self._data = None

    @pydantic.computed_field(alias='data', repr=True)
    @property
    def data_dict(self) -> dict:
        """
        The data in the form of a dictionnary.

        Useful for instance for JSON serialization
        """
        if self._data is None:
            return None
        return self._data.to_dict('list')


class BaseProfile2(BaseProfile):
    """
    Base class for all profiles except stratigraphy
    """
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
            "- Bad: undoubtedly erroneous data\n\n"
            "See :ref:`uncertainty` for details.")
    uncertainty_of_measurement: typing.Optional[float] = pydantic.Field(
        None,
        gt = 0,
        description="Quantitative uncertainty on ``data``: standard deviation or 68% confidence interval. "
        "Same units as ``data``. See :ref:`uncertainty` for details.")
    profile_nr: typing.Optional[int] = pydantic.Field(
        None, ge=0,
        description="Profile number (the lower is the higher priority)")
