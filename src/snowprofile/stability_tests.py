# -*- coding: utf-8 -*-

import typing

import pydantic


class _StabilityTest(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra='forbid')

    id: typing.Optional[str] = None
