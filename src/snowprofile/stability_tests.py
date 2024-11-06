# -*- coding: utf-8 -*-

import typing

import pydantic


class _StabilityTest(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    id: typing.Optional[str] = None


class RBStabilityTest(_StabilityTest):
    """
    Class for RB (Rutschblock) stability test.
    """


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
