# -*- coding: utf-8 -*-

import typing

import pydantic

from snowprofile._base_classes import AdditionalData, datetime_with_tz, datetime_tuple_with_tz
from snowprofile._constants import GRAIN_SHAPES


class _StabilityTest(pydantic.BaseModel):
    """
    Base class for Stability test representation.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    id: typing.Optional[str] = None
    comment: typing.Optional[str] = None
    additional_data: typing.Optional[AdditionalData] = pydantic.Field(
        None,
        description="Room to store additional data for CAAML compatibility (customData), do not use.")


class _StabilityTestResult(pydantic.BaseModel):
    """
    Base class for stability tests result representation.

    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    depth: typing.Optional[float] = pydantic.Field(
        None,
        description="Depth of the broken layer (with zero at bottom of the snowpack, in m)")
    layer_thickness: typing.Optional[float] = pydantic.Field(
        None,
        description="Thickness of the broken layer, the depth field being the top of this layer")
    grain_1: typing.Optional[typing.Literal[tuple(GRAIN_SHAPES)]] = pydantic.Field(
        None,
        description="Main grain shape of the broken layer")
    grain_2: typing.Optional[typing.Literal[tuple(GRAIN_SHAPES)]] = pydantic.Field(
        None,
        description="Secondary grain shape of the broken layer")
    grain_size: typing.Optional[float] = pydantic.Field(
        None,
        description="Grain size in the broken layer")
    grain_size_max: typing.Optional[float] = pydantic.Field(
        None,
        description="Maximum Grain size in the broken layer")
    layer_formation_time: datetime_with_tz = pydantic.Field(
        None,
        description="The formation time of the broken layer.")
    layer_formation_period: datetime_tuple_with_tz = pydantic.Field(
        (None, None),
        description="The formation period (begin, end) of the broken layer.")
    layer_comment: typing.Optional[str] = pydantic.Field(
        None,
        description="Comment associated to layer description (for CAAML compatibility only, do not fill).")
    layer_additional_data: typing.Optional[AdditionalData] = pydantic.Field(
        None,
        description="Room to store additional data for CAAML compatibility (customData), do not use.")


class RBStabilityTestResult(_StabilityTestResult):
    """
    Class for RB (Rutschblock) stability test results.
    """
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    test_score: typing.Literal[
        'RB1', 'RB2', 'RB3', 'RB4', 'RB5', 'RB6', 'RB7'] = pydantic.Field(
            description="RB result RB[1-7], RB7 meaning no fracture")
    release_type: typing.Optional[typing.Literal[
        'WB', 'MB', 'EB']] = pydantic.Field(
            None,
            description="Release type among:\n\n"
            "- WB: Whole block\n"
            "- MB: Most of the block\n"
            "- EB: Edge of the block")
    fracture_character: typing.Optional[typing.Literal[
        'SDN', 'SP', 'SC', 'RES', 'RP', 'PC', 'BRK',
        'Clean', 'Rough', 'Irregular',
        'Q1', 'Q2', 'Q3']] = pydantic.Field(
            None,
            description="")


class RBStabilityTest(_StabilityTest):
    """
    Class for RB (Rutschblock) stability test.
    """
    results: typing.List[RBStabilityTestResult] = pydantic.Field(
        [],
        description="Successive results of a single RB test. No results mean RB7.")


class CTStabilityTest(_StabilityTest):
    """
    Class for CT (Compression test) stability test.
    """


class ECTStabilityTest(_StabilityTest):
    """
    Class for ECT (Extended column test) stability test.
    """


class PSTStabilityTest(_StabilityTest):
    """
    Class for PST (Propagation Saw test) stability test.
    """


class ShearFrameStabilityTest(_StabilityTest):
    """
    Class for Shear frame stability test.
    """
