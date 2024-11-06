# -*- coding: utf-8 -*-

import typing

import pydantic
import pandas as pd

from snowprofile._base_classes import BaseProfile, BaseProfileLayered, \
    BaseProfileLayeredData, BaseProfilePointData, get_dataframe_checker
from snowprofile._constants import QUALITY_FLAGS, GRAIN_SHAPES, MANUAL_WETNESS, MANUAL_HARDNESS, \
    manual_wetness_attribution, manual_hardness_attribution


class Stratigraphy(BaseProfileLayered):
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
    """
    data: typing.Annotated[pd.DataFrame,
                           pydantic.BeforeValidator(get_dataframe_checker(grain_1=dict(type='O',
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
                                                                          uncertainty=dict(optional=True,
                                                                                           nan_allowed=True),
                                                                          quality=dict(optional=True,
                                                                                       type='O',
                                                                                       values=QUALITY_FLAGS + [None]),
                                                                          )
                                                    ),
                           pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data. Pandas DataFrame with columns are "
        "``top_depth``, ``bottom_depth``, ``thickness``, "
        "``grain_1``, ``grain_2``, ``grain_size``, ``grain_size_max``, ``hardness`` (manual hardness), ``wetness`` (manual class)"
        "and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`)")


class TemperatureProfile(BaseProfilePointData):
    method_of_measurement: typing.Optional[str] = None
    data: typing.Annotated[pd.DataFrame,
                           pydantic.BeforeValidator(get_dataframe_checker(_mode='Point',
                                                                          temperature=dict(max=0),
                                                                          uncertainty=dict(optional=True,
                                                                                           nan_allowed=True),
                                                                          quality=dict(optional=True,
                                                                                       type='O',
                                                                                       values=QUALITY_FLAGS + [None]),
                                                                          )
                                                    ),
                           pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data. Pandas DataFrame with columns are ``depth``, ``temperature`` (°C) "
        "and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`)")


class DensityProfile(BaseProfileLayeredData):
    """
    Vertical profile of density (kg/m3).
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
    data: typing.Annotated[pd.DataFrame,
                           pydantic.BeforeValidator(get_dataframe_checker(density=dict(min=0, max=917),
                                                                          uncertainty=dict(optional=True,
                                                                                           nan_allowed=True),
                                                                          quality=dict(optional=True,
                                                                                       type='O',
                                                                                       values=QUALITY_FLAGS + [None]),
                                                                          )
                                                    ),
                           pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data. Pandas DataFrame with columns are "
        "``top_depth``, ``bottom_depth``, ``thickness``, ``density`` (kg/m3) "
        "and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`)")


class LWCProfile(BaseProfileLayeredData):
    """
    Vertical profile of LWC (Liquid water content, % by volume).
    """
    method_of_measurement: typing.Optional[typing.Literal[
        "Denoth Probe", "Snow Fork", "SnowPro Probe", "WISe", "other dielectric permittivity method",
        "MRI", "other"]] = pydantic.Field(
            None,
            description="Measurement method")
    probed_thickness: typing.Optional[float] = pydantic.Field(
        None,
        description="Probe thickness (vertical dimension of measurement, m)")
    data: typing.Annotated[pd.DataFrame,
                           pydantic.BeforeValidator(get_dataframe_checker(lwc=dict(min=0, max=100),
                                                                          uncertainty=dict(optional=True,
                                                                                           nan_allowed=True),
                                                                          quality=dict(optional=True,
                                                                                       type='O',
                                                                                       values=QUALITY_FLAGS + [None]),
                                                                          )
                                                    ),
                           pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data. Pandas DataFrame with columns are "
        "``top_depth``, ``bottom_depth``, ``thickness``, ``lwc`` (% vol.) "
        "and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`)")


class _SSAProfile(BaseProfile):
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


class SSAProfile(BaseProfileLayeredData, _SSAProfile):
    """
    Vertical profile of SSA (Specific surface area, m2/kg), measured on layers.
    """
    data: typing.Annotated[pd.DataFrame,
                           pydantic.BeforeValidator(get_dataframe_checker(ssa=dict(min=0),
                                                                          uncertainty=dict(optional=True,
                                                                                           nan_allowed=True),
                                                                          quality=dict(optional=True,
                                                                                       type='O',
                                                                                       values=QUALITY_FLAGS + [None]),
                                                                          )
                                                    ),
                           pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data. Pandas DataFrame with columns are "
        "``top_depth``, ``bottom_depth``, ``thickness``, ``ssa`` (m2/kg) "
        "and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`)")


class SSAPointProfile(BaseProfilePointData, _SSAProfile):
    """
    Vertical profile of SSA (Specific surface area, m2/kg), measured on points.
    """
    data: typing.Annotated[pd.DataFrame,
                           pydantic.BeforeValidator(get_dataframe_checker(_mode='Point',
                                                                          ssa=dict(min=0),
                                                                          uncertainty=dict(optional=True,
                                                                                           nan_allowed=True),
                                                                          quality=dict(optional=True,
                                                                                       type='O',
                                                                                       values=QUALITY_FLAGS + [None]),
                                                                          )
                                                    ),
                           pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data. Pandas DataFrame with columns are ``depth``, ``ssa`` (m2/kg) "
        "and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`)")


class _HardnessProfile(BaseProfileLayeredData):
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
    """
    data: typing.Annotated[pd.DataFrame,
                           pydantic.BeforeValidator(get_dataframe_checker(hardness=dict(min=0),
                                                                          uncertainty=dict(optional=True,
                                                                                           nan_allowed=True),
                                                                          quality=dict(optional=True,
                                                                                       type='O',
                                                                                       values=QUALITY_FLAGS + [None]),
                                                                          )
                                                    ),
                           pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data. Pandas DataFrame with columns are "
        "``top_depth``, ``bottom_depth``, ``thickness``, ``hardness`` (N) "
        "and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`)")


class RamSondeProfile(_HardnessProfile):
    """
    Special type of Hardness profile for RamSonde measurements
    """
    data: typing.Annotated[pd.DataFrame,
                           pydantic.BeforeValidator(get_dataframe_checker(hardness=dict(min=0, optional=True),
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
                                                    ),
                           pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data. Pandas DataFrame with columns are "
        "``top_depth``, ``bottom_depth``, ``thickness``, ``hardness`` (N), "
        "``weight_hammer``, ``weight_tube``, ``n_drops``, ``drop_height`` "
        "and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`)")
    # TODO: Computation of hardness from other data ?  <06-11-24, Léo Viallon-Galinier> #


class StrengthProfile(BaseProfileLayeredData):
    """
    Vertical profile of strength (N).
    """
    method_of_measurement: typing.Optional[typing.Literal[
        "Shear Frame",
        "other"]] = pydantic.Field(
            None,
            description="Measurement method")
    probed_area: typing.Optional[float] = pydantic.Field(
        None,
        description="Probed area (m2)")
    data: typing.Annotated[pd.DataFrame,
                           pydantic.BeforeValidator(get_dataframe_checker(strength=dict(min=0),
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
                                                    ),
                           pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data. Pandas DataFrame with columns are "
        "``top_depth``, ``bottom_depth``, ``thickness``, ``strength`` (N), ``fracture_character`` (optional) "
        "and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`).\n\n"
        "Fracture character are one of the following possibilities:\n\n"
        "- SP: Sudden planar\n"
        "- SC: Sudden collapse\n"
        "- SDN: Sudden (both)\n"
        "- RP: Resistant planar\n"
        "- PC: Progressive compression\n"
        "- RES: Resistant (both)\n"
        "- BRK or B: Break\n"
        "- X: Other/Unknown\n")


class ImpurityProfile(BaseProfileLayeredData):
    """
    Vertical profile of impurities (mass or volume fraction).
    """
    method_of_measurement: typing.Optional[typing.Literal[
        "other"]] = pydantic.Field(
            None,
            description="Measurement method")
    impurity_type: typing.Literal[
        "Black Carbon", "Dust", "Isotopes", "Other"] = pydantic.Field(
            description="Impurity type for the profile")
    unit: typing.Literal[
        "mass fraction", "volume fraction"] = pydantic.Field(
            "mass fraction",
            descritpion="Unit for measurement mass or volume fraction")
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
    data: typing.Annotated[pd.DataFrame,
                           pydantic.BeforeValidator(get_dataframe_checker(mass_fraction=dict(min=0, max=100,
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
                                                    ),
                           pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data. Pandas DataFrame with columns are "
        "``top_depth``, ``bottom_depth``, ``thickness``, ``mass_fraction`` or ``volume_fraction`` "
        "and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`)")


class OtherScalarProfile(BaseProfileLayeredData):
    """
    Other profile of scalar data (not covered by other Profile class).
    """
    method_of_measurement: typing.Optional[str] = None
    unit: str = pydantic.Field(
        description="Unit (SI unit please)")
    parametrer: str = pydantic.Field(
        description="Measured parameter")
    data: typing.Annotated[pd.DataFrame,
                           pydantic.BeforeValidator(get_dataframe_checker(data=dict(),
                                                                          uncertainty=dict(optional=True,
                                                                                           nan_allowed=True),
                                                                          quality=dict(optional=True,
                                                                                       type='O',
                                                                                       values=QUALITY_FLAGS + [None]),
                                                                          )
                                                    ),
                           pydantic.json_schema.SkipJsonSchema()] = pydantic.Field(
        description="The profile data. Pandas DataFrame with columns are "
        "``top_depth``, ``bottom_depth``, ``thickness``, ``data`` "
        "and optionnally ``uncertainty`` (quantitative, same unit as data) or ``quality`` (see :ref:`uncertainty`)")


class OtherVectorialProfile(OtherScalarProfile):
    """
    Other profile of vectorial data (data inherently multi-dimensional, with same unit and type).
    """
    rank: int = pydantic.Field(
        gt = 1,
        description="Length of the vector (>1, otherwise use OtherScalarProfile)")
