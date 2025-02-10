# -*- coding: utf-8 -*-

import typing

import pydantic

from snowprofile._base_classes import BaseProfile, BaseProfile2
from snowprofile._constants import QUALITY_FLAGS, GRAIN_SHAPES, MANUAL_WETNESS, MANUAL_HARDNESS, \
    manual_wetness_attribution, manual_hardness_attribution

__all__ = ['Stratigraphy',
           'TemperatureProfile', 'DensityProfile', 'LWCProfile',
           'SSAProfile', 'SSAPointProfile',
           'HardnessProfile', 'RamSondeProfile',
           'StrengthProfile', 'ImpurityProfile',
           'ScalarProfile', 'VectorialProfile']


class Stratigraphy(BaseProfile):
    """
    Stratigraphic measurement per layer:

    - Grain shape
    - hardness, on the scale (intermediates are allowed, details in Fierz et al., 2009):
        - F: Fist (1)
        - 4F : 4 Fingers (2)
        - 1F : 1 finger (3)
        - P : Pencil (4)
        - K : Knife (5)
    - wetness, on the scale (intermediates are allowed, details in Fierz et al., 2009):
        - D : Dry (1)
        - M : Moist (2)
        - W : Wet (3)
        - V : Very wet (4)
        - S : Soaked (5)

    The data contains:

    - ``top_height``
    - ``bottom_height``
    - ``thickness``
    - ``grain_1``
    - ``grain_2``
    - ``grain_size``
    - ``grain_size_max``
    - ``hardness`` (manual hardness)
    - ``wetness`` (manual class)

    and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).
    """
    _data_config = dict(
        grain_1=dict(type='O',
                     values=GRAIN_SHAPES + [None]),
        grain_2=dict(type='O',
                     values=GRAIN_SHAPES + [None]),
        grain_size=dict(min=0,
                        nan_allowed=True),
        grain_size_max=dict(min=0,
                            optional=True,
                            nan_allowed=True),
        hardness=dict(type='O',
                      values=MANUAL_HARDNESS + [None],
                      translate=manual_hardness_attribution,
                      ),
        wetness=dict(type='O',
                     values=MANUAL_WETNESS + [None],
                     translate=manual_wetness_attribution,
                     ),
        loc=dict(type='O',
                 optional=True,
                 values=['no', 'top', 'bottom', 'all', 'true', 'false']),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
        comment=dict(optional=True,
                     type='O', ),
        additional_data=dict(optional=True,
                             type='O', ),
        formation_time=dict(optional=True,
                            type='O'),
        formation_period_begin=dict(optional=True,
                                    type='O'),
        formation_period_end=dict(optional=True,
                                  type='O'),
    )


class TemperatureProfile(BaseProfile2):
    """
    Temperature profile: ensemble of points and temperature measurements

    The data contains:

    - ``height``
    - ``temperature`` (°C)

    and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).
    """
    method_of_measurement: typing.Optional[str] = None
    _data_config = dict(
        _mode='Point',
        temperature=dict(max=0),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )


class DensityProfile(BaseProfile2):
    """
    Vertical profile of density (kg/m3).

    The data contains:

    - ``top_height``
    - ``bottom_height``
    - ``thickness``
    - ``density`` (kg/m3)

    and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).
    """
    method_of_measurement: typing.Optional[typing.Literal[
        "Snow Tube", "Snow Cylinder", "Snow Cutter", "Snow wedge Cutter", "other gravimetric measurement method",
        "Denoth Probe", "SnowPro Probe", "Snow Fork", "other dielectric permittivity method",
        "Tomography", "SMP", "Neutron scattering probe",
        "other"]] = pydantic.Field(
            None,
            description="Measurement method")
    probed_volume: typing.Optional[float] = pydantic.Field(
        None,
        description="Probe volume (m3)")
    probed_diameter: typing.Optional[float] = pydantic.Field(
        None,
        description="Probe volume (m)")
    probed_length: typing.Optional[float] = pydantic.Field(
        None,
        description="Probe length (m)")
    probed_thickness: typing.Optional[float] = pydantic.Field(
        None,
        description="Probe thickness (vertical dimension, m)")
    _data_config = dict(
        density=dict(min=0, max=917),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )


class LWCProfile(BaseProfile2):
    """
    Vertical profile of LWC (Liquid water content, % by volume).

    The data contains:

    - ``top_height``
    - ``bottom_height``
    - ``thickness``
    - ``lwc`` (% vol.)

    and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).
    """
    method_of_measurement: typing.Optional[typing.Literal[
        "Denoth Probe", "Snow Fork", "SnowPro Probe", "WISe", "other dielectric permittivity method",
        "MRI", "other"]] = pydantic.Field(
            None,
            description="Measurement method")
    probed_thickness: typing.Optional[float] = pydantic.Field(
        None,
        description="Probe thickness (vertical dimension of measurement, m)")
    _data_config = dict(
        lwc=dict(min=0, max=100),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )


class _SSAProfile(BaseProfile2):
    """
    Vertical profile of SSA (Specific surface area, m2/kg).

    Base class for SSA, whether the profile is a point profile or a layer profile.
    """
    method_of_measurement: typing.Optional[typing.Literal[
        "Ice Cube", "IRIS", "InfraSnow", "DUFFISSS-1310", "DUFFISSS-1550",
        "HISSGraS", "ASSSAP", "other IR integrating sphere",
        "SWIRcam", "SnowImager", "other NIR method",
        "Tomography", "SMP",
        "other"]] = pydantic.Field(
            None,
            description="Measurement method")
    probed_thickness: typing.Optional[float] = pydantic.Field(
        None,
        description="Probe thickness (vertical dimension of measurement, m)")


class SSAProfile(_SSAProfile):
    """
    Vertical profile of SSA (Specific surface area, m2/kg), measured on layers.

    The data contains:

    - ``top_height``
    - ``bottom_height``
    - ``thickness``
    - ``ssa`` (m2/kg)

    and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).
    """
    _data_config = dict(
        ssa=dict(min=0),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )


class SSAPointProfile(_SSAProfile):
    """
    Vertical profile of SSA (Specific surface area, m2/kg), measured on points.

    The data contains:

    - ``height``
    - ``ssa`` (m2/kg)

    and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).
    """
    _data_config = dict(
        _mode='Point',
        ssa=dict(min=0),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )


class _HardnessProfile(BaseProfile2):
    """
    Vertical profile of hardness (N).

    Base class for both RAMSONDE profile or simple hardness profile from other source.
    """
    method_of_measurement: typing.Optional[typing.Literal[
        "SnowMicroPen", "Ram Sonde", "Push-Pull Gauge",
        "Avatech SP1", "Avatech SP2", "Scope propagation labs",
        "other automatic penetrometer",
        "other"]] = pydantic.Field(
            None,
            description="Measurement method")


class HardnessProfile(_HardnessProfile):
    """
    Vertical profile of hardness (N).

    The data contains:

    - ``top_height``
    - ``bottom_height``
    - ``thickness``
    - ``hardness`` (N)

    and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).
    """
    _data_config = dict(
        hardness=dict(min=0),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )


class RamSondeProfile(_HardnessProfile):
    """
    Special type of Hardness profile for RamSonde measurements

    The data contains:

    - ``top_height``
    - ``bottom_height``
    - ``thickness``
    - ``hardness`` (N)
    - ``weight_hammer``
    - ``weight_tube``
    - ``n_drops``
    - ``drop_height``

    and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).
    """
    _data_config = dict(
        hardness=dict(min=0, optional=True),
        weight_hammer=dict(min=0),
        weight_tube=dict(min=0),
        n_drops=dict(type=int, min=0),
        drop_height=dict(min=0),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )
    # TODO: Computation of hardness from other data ?  <06-11-24, Léo Viallon-Galinier> #


class StrengthProfile(BaseProfile2):
    """
    Vertical profile of strength (N).

    The data contains:


    - ``top_height``
    - ``bottom_height``
    - ``thickness``
    - ``strength`` (N)
    - ``fracture_character`` (optional)

    and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).

    Fracture character are one of the following possibilities:

    - SP: Sudden planar
    - SC: Sudden collapse
    - SDN: Sudden (both)
    - RP: Resistant planar
    - PC: Progressive compression
    - RES: Resistant (both)
    - BRK or B: Break
    - X: Other/Unknown
    """
    method_of_measurement: typing.Optional[typing.Literal[
        "Shear Frame",
        "other"]] = pydantic.Field(
            None,
            description="Measurement method")
    strength_type: typing.Optional[typing.Literal[
        "compressive", "tensile", "shear", "mixed", "other"]] = pydantic.Field(
            None,
            description="Shear direction: compressive, tensile, shear, other or mixed")
    probed_area: typing.Optional[float] = pydantic.Field(
        None,
        description="Probed area (m2)")
    _data_config = dict(
        strength=dict(min=0),
        fracture_character=dict(optional=True,
                                nan_allowed=True,
                                values=["SDN", "SP",
                                        "SC", "RES",
                                        "PC", "RP",
                                        "BRK", "B",
                                        "X", None],
                                type='O'),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )


class ImpurityProfile(BaseProfile2):
    """
    Vertical profile of impurities (mass or volume fraction).

    The data contains:

    - ``top_height``
    - ``bottom_height``
    - ``thickness``
    - ``mass_fraction`` or ``volume_fraction``

    and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).
    """
    method_of_measurement: typing.Optional[typing.Literal[
        "other"]] = pydantic.Field(
            None,
            description="Measurement method")
    impurity_type: typing.Literal[
        "Black Carbon", "Dust", "Isotopes", "Other"] = pydantic.Field(
            description="Impurity type for the profile")
    probed_volume: typing.Optional[float] = pydantic.Field(
        None,
        description="Probe volume (m3)")
    probed_diameter: typing.Optional[float] = pydantic.Field(
        None,
        description="Probe volume (m)")
    probed_length: typing.Optional[float] = pydantic.Field(
        None,
        description="Probe length (m)")
    probed_thickness: typing.Optional[float] = pydantic.Field(
        None,
        description="Probe thickness (vertical dimension, m)")
    _data_config = dict(
        mass_fraction=dict(min=0, max=100,
                           optional=True,
                           nan_allowed=True),
        volume_fraction=dict(min=0, max=100,
                             optional=True,
                             nan_allowed=True),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )


class ScalarProfile(BaseProfile2):
    """
    Other profile of scalar data (not covered by other Profile class).

    The data contains:

    - ``top_height``
    - ``bottom_height``
    - ``thickness``
    - ``data``

    and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).
    """
    method_of_measurement: typing.Optional[str] = None
    unit: str = pydantic.Field(
        description="Unit (SI unit please)")
    parameter: str = pydantic.Field(
        description="Measured parameter")
    _data_config = dict(
        data=dict(),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )


class VectorialProfile(ScalarProfile):
    """
    Other profile of vectorial data (data inherently multi-dimensional, with same unit and type).

    ``data`` is a list or numpy array
    """
    rank: int = pydantic.Field(
        gt = 1,
        description="Length of the vector (>1, otherwise use OtherScalarProfile)")
    _data_config = dict(
        data=dict(type='O'),
        uncertainty=dict(optional=True,
                         nan_allowed=True),
        quality=dict(optional=True,
                     type='O',
                     values=QUALITY_FLAGS + [None]),
    )
