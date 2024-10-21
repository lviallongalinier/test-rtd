# -*- coding: utf-8 -*-

import typing

import pydantic

from snowprofile._base_classes import BaseProfile, BaseProfileLayered, \
    BaseProfileLayeredData, BaseProfilePointData


class Stratigraphy(BaseProfileLayered):
    """
    Stratigraphic measurement per layer:

    - top_deptha (zero at bottom)
    - thicknesses/bottom_depth (zero at bottom)
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
    pass


class TemperatureProfile(BaseProfilePointData):
    method_of_measurement: typing.Optional[str] = None
    # TODO: tbd  <17-10-24, Léo Viallon-Galinier> #


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


class _SSAProfile(BaseProfile):
    # TODO: This is points or Layers !!  <18-10-24, Léo Viallon-Galinier> #
    """
    Vertical profile of SSA (Specific surface area, m2/kg).
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


class SSAPointProfile(BaseProfilePointData, _SSAProfile):
    """
    Vertical profile of SSA (Specific surface area, m2/kg), measured on points.
    """


class HardnessProfile(BaseProfileLayeredData):
    """
    Vertical profile of hardness (N).
    """
    # TODO: Data could be hardness or detailed  <18-10-24, Léo Viallon-Galinier> #
    method_of_measurement: typing.Optional[typing.Literal[
        "SnowMicroPen", "Ram Sonde", "Push-Pull Gauge",
        "Avatech SP1", "Avatech SP2", "Scope propagation labs",
        "other automatic penetrometer",
        "other"]] = pydantic.Field(
            None,
            description="Measurement method")


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
    fracture_character: typing.Optional[typing.List[typing.Literal[
        "SDN", "SP", "SC", "RES", "PC", "RP", "BRK", "B", "X"]]] = pydantic.Field(
            None,
            description="Fracture type among:\n\n"
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
    Vertical profile of impurities (mass or volume fraction, default being mass fraction).
    """
    method_of_measurement: typing.Optional[typing.Literal[
        "Shear Frame",
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


class OtherScalarProfile(BaseProfileLayeredData):
    """
    Other profile of scalar data (not covered by other Profile class).
    """
    method_of_measurement: typing.Optional[str] = None
    unit: str = pydantic.Field(
        description="Unit (SI unit please)")
    parametrer: str = pydantic.Field(
        description="Measured parameter")


class OtherVectorialProfile(OtherScalarProfile):
    """
    Other profile of vectorial data (data inherently multi-dimensional, with same unit and type).
    """
    rank: int = pydantic.Field(
        gt = 1,
        description="Length of the vector (>1, otherwise use OtherScalarProfile)")
