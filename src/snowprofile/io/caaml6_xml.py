# -*- coding: utf-8 -*-

import logging
import xml.etree.ElementTree as ET
import re


def read_caaml6_xml(filename):
    """
    Parse a CAAML 6 XML-based IACS Snow Profile document and return the associated SnowProfile object.

    Versions up to 6.0.5 are supported.

    this parser correctly deal with XML namespaces. One unique namespace URI have to be used for CAAML tags across
    the entire XML file for the parser to work correctly.

    Most of the data stored in the CAAML format is parsed. However, some specific corner cases are not
    covered by this parser. Specifically, as CAAML work with depth and the snowprofile package use
    height, and the total depth is not compulsory in the CAAML format, the total depth may be set to 0
    and the layer top/bottom height may be negative values. Some other corner cases and additional data
    could not be parsed by this package. However, all main data treated by NiViz is fully parsed
    (and even much more metadata is correctly treated).

    Some data is partially parsed. For instance, lacking numeric data could be specified as
    inapplicable (there is no value), missing (the value is not available when writting the data and may not exist),
    template (the value will be available later), unknown (the value is not available to the writter of the data but
    exists) or withheld (th evalue cannot be divulged). All these cases are treated the same way, by using a ``None``
    python value.

    Hence, reading a CAAML file and rewritting it with this package may cause some corner data loss.

    :param filename: File path of the CAAML/XML document to parse
    :type filename: str
    :returns: The associated SnowProfile python object (or None in case of errors)
    :rtype: SnowProfile or None
    """
    # XML parsing
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
    except ET.ParseError as e:
        logging.error(f"Fail to parse CAAML XML-based document {filename}. Error while parsing XML file: {str(e)}")
        return None
    # Identification of CAAML namespace
    if root.tag == "SnowProfile":  # Case no namespace
        ns = None
        nss = ''
    else:
        r = re.match('{(.*)}SnowProfile$', root.tag)
        if r is None:
            logging.error(f"The root element of {filename} is not a SnowProfile element. "
                          "This is not a valid CAAML file.")
            return None
        else:
            ns = r.group(1)
            nss = '{' + ns + '}'
    logging.debug(f"Parsing {filename}. Found CAAML namespace as {nss}")

    # Parsing part by part
    from snowprofile import SnowProfile
    from snowprofile.classes import Time, Observer, Location, Environment, Weather, SurfaceConditions

    # - Time
    time = Time(
        record_time=_parse_str(root, f'{nss}timeRef/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
        record_period=(
            _parse_str(root, f'{nss}timeRef/{nss}recordTime/{nss}TimePeriod/{nss}beginPosition'),
            _parse_str(root, f'{nss}timeRef/{nss}recordTime/{nss}TimePeriod/{nss}endPosition')),
        report_time=_parse_str(root, f'{nss}timeRef/{nss}dateTimeReport'),
        last_edition_time=_parse_str(root, f'{nss}timeRef/{nss}dateTimeLastEdit'),
        comment=_parse_str(root, f'{nss}timeRef/{nss}metaData/{nss}comment'),
        additional_data=_parse_additional_data(root.find(f'{nss}timeRef/{nss}customData'), namespace=ns))

    # - Observer
    observer = Observer(
        source_id=root.find(f'{nss}Operation/'),
        source_name=_parse_str(root, f'{nss}srcRef/{nss}Operation/{nss}name'),
        source_comment=_parse_str(root, f'{nss}srcRef/{nss}Operation/{nss}metaData/{nss}comment'),
        source_additional_data = _parse_additional_data(root.find(f'{nss}srcRef/{nss}Operation/{nss}customData'),
                                                        namespace=ns))
    contact_persons_1 = root.findall(f'{nss}srcRef/{nss}Operation/{nss}contactPerson')
    contact_persons_2 = root.findall(f'{nss}srcRef/{nss}Person')
    contact_persons = []
    if contact_persons_1 is not None:
        for p in contact_persons_1:
            contact_persons.append(_parse_contact_person(p, nss=nss, ns=ns))
    if contact_persons_2 is not None:
        for p in contact_persons_2:
            contact_persons.append(_parse_contact_person(p, nss=nss, ns=ns))
    if len(contact_persons) > 0:
        observer.contact_persons = contact_persons

    # - Location
    loc = root.find(f'{nss}locRef')
    lat, lon = _parse_lat_lon(loc.find(f'{nss}pointLocation'))
    location = Location(
        id=_search_gml_id(loc),
        name=_parse_str(root, f'{nss}locRef/{nss}name'),
        point_type=_parse_str(root, f'{nss}locRef/{nss}obsPointSubType'),
        aspect=_parse_numeric(root, f'{nss}locRef/{nss}validAspect'),
        elevation=_parse_numeric(root, f'{nss}locRef/{nss}validElevation'),
        slope=_parse_numeric(root, f'{nss}locRef/{nss}validSlopeAngle'),
        latitude=lat,
        longitude = lon,
        country=_parse_str(root, f'{nss}locRef/{nss}country'),
        region=_parse_str(root, f'{nss}locRef/{nss}region'),
        additional_data=_parse_additional_data(root.find(f'{nss}locRef/{nss}customData'), namespace=ns))

    # - Environment
    environment = Environment(
        solar_mask=_parse_solar_mask(root.find(f'{nss}locRef/{nss}solarMask'), nss=nss),
        solar_mask_method_of_measurement=_parse_str(root, f'{nss}locRef/{nss}solarMask/{nss}solarMaskMetaData/{nss}methodOfMeas'),
        solar_mask_uncertainty=_parse_numeric(root, f'{nss}locRef/{nss}solarMask/{nss}solarMaskMetaData/{nss}uncertaintyOfMeas'),
        solar_mask_quality=_parse_numeric(root, f'{nss}locRef/{nss}solarMask/{nss}solarMaskMetaData/{nss}qualityOfMeas'),
        solar_mask_comment=_parse_str(root, f'{nss}locRef/{nss}solarMask/{nss}solarMaskMetaData/{nss}comment'),
        solar_mask_additional_data=_parse_additional_data(root.find(f'{nss}locRef/{nss}solarMask/{nss}customData'),
                                                          namespace=ns),
        bed_surface=_parse_str(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}bedSurface'),
        bed_surface_comment=_parse_str(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}bedSurfaceComment'),
        litter_thickness=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}litterThickness'),
        ice_thickness=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}iceThickness'),
        low_vegetation_height=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}lowVegetationHeight'),
        LAI=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}lai'),
        forest_presence=_parse_str(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}forestPresence'),
        forest_presence_comment=_parse_str(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}forestComment'),
        sky_view_factor=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}skyViewFactor'),
        tree_height=_parse_numeric(root, f'{nss}locRef/{nss}obsPointEnvironment/{nss}treeHeight'))

    # - Weather
    base = f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}weatherCond'
    weather = Weather(
        cloudiness=_parse_str(root, f'{base}/{nss}skiCond'),
        precipitation=_parse_str(root, f'{base}/{nss}precipTI'),
        air_temperature=_parse_numeric(root, f'{base}/{nss}airTempPres'),
        wind_speed=_parse_numeric(root, f'{base}/{nss}windSpd'),
        wind_direction=_parse_numeric(root, f'{base}/{nss}windDir'),
        air_temperature_measurement_height=_parse_numeric(
            root,
            f'{base}/{nss}metaData/{nss}airTempMeasurementHeight'),
        wind_measurement_height=_parse_numeric(
            root,
            f'{base}/{nss}metaData/{nss}windMeasurementHeight'),
        comment = _parse_str(
            root,
            f'{base}/{nss}metaData/{nss}comment'),
        additional_data=_parse_additional_data(root.find(
            f'{base}/{nss}customData'), namespace=ns))

    # - Surface Conditions
    base = f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}surfCond'
    surface_conditions = SurfaceConditions(
        surface_roughness=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}surfRoughness'),
        surface_wind_features=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}surfWindFeatures'),
        surface_melt_rain_features=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}surfMeltRainFeatures'),
        surface_features_amplitude=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validAmplitude/{nss}AmplitudePosition/{nss}position',
            factor=0.01),  # cm -> m
        surface_features_amplitude_min=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validAmplitude/{nss}AmplitudeRange/{nss}beginPosition',
            factor=0.01),  # cm -> m
        surface_features_amplitude_max=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validAmplitude/{nss}AmplitudeRange/{nss}endPosition',
            factor=0.01),  # cm -> m
        surface_features_wavelength=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validWavelength/{nss}WavelengthPosition/{nss}position',
            factor=0.01),  # cm -> m
        surface_features_wavelength_min=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validWavelength/{nss}WavelengthRange/{nss}beginPosition',
            factor=0.01),  # cm -> m
        surface_features_wavelength_max=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validWavelength/{nss}WavelengthRange/{nss}endPosition',
            factor=0.01),  # cm -> m
        surface_features_aspect=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}Components/{nss}validAspect/{nss}position'),
        penetration_ram=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}penetrationRam',
            factor=0.01),  # cm -> m
        penetration_foot=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}penetrationFoot',
            factor=0.01),  # cm -> m
        penetration_ski=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}penetrationSki',
            factor=0.01),  # cm -> m
        lap_presence=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}lapPresence'),
        surface_temperature=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}surfTemp/{nss}data'),
        surface_temperature_measurement_method=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}surfTemp/{nss}methodOfMeas'),
        surface_albedo=_parse_numeric(
            root,
            f'{base}/{nss}surfFeatures/{nss}surfAlbedo/{nss}albedo/{nss}albedoMeasurement'),
        surface_albedo_comment=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}surfAlbedo/{nss}albedo/{nss}metaData/{nss}comment'),
        spectral_albedo=_parse_spectral_albedo(
            root.findall(
                f'{base}/{nss}surfFeatures/{nss}surfAlbedo/{nss}spectralAlbedo'),
            nss=nss),
        spectral_albedo_comment=_parse_str(
            root,
            f'{base}/{nss}surfFeatures/{nss}surfAlbedo/{nss}spectralAlbedo/{nss}metaData/{nss}comment'),
        comment=_parse_str(
            root,
            f'{base}/{nss}metaData/{nss}comment'),
        additional_data=_parse_additional_data(root.find(
            f'{base}/{nss}customData'), namespace=ns))

    # Creating SnowProfile object
    base = f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}snowPackCond'

    profile_depth = _parse_numeric(
        root,
        f'{base}/{nss}hS/{nss}Components/{nss}height',
        factor=0.01)  # cm -> m

    sp = SnowProfile(
        id=_search_gml_id(root),
        comment=_parse_str(root, f'{nss}metaData/{nss}comment'),
        profile_comment=_parse_str(
            root,
            f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}metaData/{nss}comment'),
        time=time,
        observer=observer,
        location=location,
        environment=environment,
        weather=weather,
        surface_conditions=surface_conditions,
        application=_parse_str(root, f'{nss}application'),
        application_version=_parse_str(root, f'{nss}applicaationVersion'),
        profile_depth=profile_depth,
        profile_depth_std=_parse_numeric(
            root,
            f'{base}/{nss}hSVariability/{nss}Components/{nss}height',
            factor=0.01),
        profile_swe=_parse_numeric(
            root,
            f'{base}/{nss}hS/{nss}Components/{nss}waterEquivalent',
            factor=1),  # kg/m2 is the only one accepted
        profile_swe_std=_parse_numeric(
            root,
            f'{base}/{nss}hSVariability/{nss}Components/{nss}waterEquivalent',
            factor=1),
        new_snow_24_depth=_parse_numeric(
            root,
            f'{base}/{nss}hN24/{nss}Components/{nss}height',
            factor=0.01),  # cm -> m
        new_snow_24_depth_std=_parse_numeric(
            root,
            f'{base}/{nss}hIN/{nss}Components/{nss}height',
            factor=0.01),
        new_snow_24_swe=_parse_numeric(
            root,
            f'{base}/{nss}hN24/{nss}Components/{nss}waterEquivalent',
            factor=1),
        new_snow_24_swe_std=_parse_numeric(
            root,
            f'{base}/{nss}hIN/{nss}Components/{nss}waterEquivalent',
            factor=1),
        snow_transport=_parse_str(
            root,
            f'{base}/{nss}snowTransport'),
        snow_transport_occurence_24=_parse_numeric(
            root,
            f'{base}/{nss}snowTransportOccurence24'),
        stratigraphy_profile = _parse_stratigraphy(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}stratProfile'),
            nss=nss, profile_depth=profile_depth),
        temperature_profiles = _parse_temperature_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}tempProfile'),
            nss=nss, profile_depth=profile_depth),
        density_profiles = _parse_density_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}densityProfile'),
            nss=nss, profile_depth=profile_depth),
        lwc_profiles = _parse_lwc_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}lwcProfile'),
            nss=nss, profile_depth=profile_depth),
        ssa_profiles = _parse_ssa_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}specSurfAreaProfile'),
            nss=nss, profile_depth=profile_depth),
        hardness_profiles = _parse_hardness_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}hardnessProfile'),
            nss=nss, profile_depth=profile_depth),
        strength_profiles = _parse_strength_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}strengthProfile'),
            nss=nss, profile_depth=profile_depth),
        impurity_profiles = _parse_impurity_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}impurityProfile'),
            nss=nss, profile_depth=profile_depth),
        other_scalar_profiles = _parse_other_scalar_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}otherScalarProfile'),
            nss=nss, profile_depth=profile_depth),
        other_vectorial_profiles = _parse_other_vectorial_profiles(
            root.findall(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}otherVectorialProfile'),
            nss=nss, profile_depth=profile_depth),
        stability_tests = _parse_stability_tests(
            root.find(f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}stbTests'),
            nss=nss, profile_depth=profile_depth),
        additional_data=_parse_additional_data(root.find(
            f'{nss}customData'), namespace=ns),
        profiles_additional_data = _parse_additional_data(root.find(
            f'{nss}snowProfileResultsOf/{nss}SnowProfileMeasurements/{nss}customData'), namespace=ns))

    return sp


def _parse_str(root, path, clean=True, attribute=None):
    """
    Search for an element described by path in the XML Element root
    and parse its content as a string.

    :param root: A XML Element (or None)
    :param path: Path to the searched data (str or list, in case this is a list, take the first non-void element)
    :param clean: Apply strip() on the resulting string
    :param attribute: Parse the content of an attribute of the given element rather than the text content.
    :returns: Parsed string or None if not found
    """
    if isinstance(path, list):
        for p in path:
            f = root.find(p)
            if f is not None:
                break
    else:
        f = root.find(path)

    if f is not None:
        if attribute is None:
            r = f.text
        else:
            if attribute in f.attrib:
                r = f.attrib[attribute]
            else:
                return None
        if clean and r is not None:
            return r.strip()
        else:
            return r


def _parse_numeric(root, path, factor=1, attribute=None):
    """
    Search for an element described by path in the XML Element root
    and parse its content as a floating-point number.

    :param root: A XML Element (or None)
    :param path: Path to the searched data
    :param factor: A factor to apply to the parsed float
    :param attribute: Parse the content of an attribute of the given element rather than the text content.
    :returns: Parsed float or None if not found
    """
    if isinstance(path, list):
        for p in path:
            f = root.find(p)
            if f is not None:
                break
    else:
        f = root.find(path)

    if f is not None:
        if attribute is None:
            r = f.text.strip()
        else:
            if attribute in f.attrib:
                r = f.attrib[attribute]
            else:
                return None
        try:
            f = float(r)
            return f * factor
        except Exception:
            return None


def _parse_numeric_list(root, path, factor=1, attribute=None):
    """
    Search for an element described by path in the XML Element root
    and parse its content as a list of floating-point number.

    :param root: A XML Element (or None)
    :param path: Path to the searched data
    :param factor: A factor to apply to the parsed float
    :param attribute: Parse the content of an attribute of the given element rather than the text content.
    :returns: Parsed list of float or None if not found
    """
    if isinstance(path, list):
        for p in path:
            f = root.find(p)
            if f is not None:
                break
    else:
        f = root.find(path)

    if f is not None:
        if attribute is None:
            r = f.text.strip()
        else:
            if attribute in f.attrib:
                r = f.attrib[attribute]
            else:
                return None
        try:
            fl = r.split()
            rl = [float(x) * factor for x in fl]
            return rl
        except Exception:
            return None


def _search_gml_id(element):
    if element is None:
        return None
    for key, value in element.attrib.items():
        r = re.match('{.*}id$', key)
        if r is not None or key == 'id':
            return value


def _parse_lat_lon(pointlocation):
    if pointlocation is None:
        return None, None
    for elem in pointlocation:
        r = re.match('{.*}Point$', elem.tag)
        if r is not None or elem.tag == 'Point':
            for e in elem:
                r = re.match('{.*}pos$', e.tag)
                if r is not None or e.tag == 'pos':
                    try:
                        sp = e.text.strip().split()
                        return float(sp[0]), float(sp[1])
                    except Exception:
                        logging.warning('Could not parse latitude/longitude')

    logging.error('Could not parse latitude/longitude. Will use 0, 0.')
    return 0, 0


def _parse_list(*args, **kwargs):
    r = _parse_str(*args, **kwargs)
    if r is None:
        return []
    else:
        return r.split()


def _parse_additional_data(ad_element, namespace=None, origin='caamlxml6'):
    if ad_element is not None:
        data = ''
        for e in ad_element:
            data += ET.tostring(e, encoding='utf-8').decode('utf-8')
        return {'data': data, 'origin': origin}
    return None


def _parse_contact_person(p, nss='', ns=None):
    if p is None:
        return None
    from snowprofile.classes import Person
    return Person(
        id=_search_gml_id(p),
        name=_parse_str(p, f'{nss}name'),
        comment=_parse_str(p, '{nss}metaData/{nss}comment'),
        additional_data=_parse_additional_data(p.find(f'{nss}customData'), namespace=ns))


def _parse_solar_mask(sm_element, nss=''):
    if sm_element is None:
        return None

    from snowprofile.classes import SolarMask

    data = _parse_generic_profile(
        sm_element.findall(f'{nss}Data'),
        {'azimuth': {'path': f'{nss}azimuth', 'type': 'numeric'},
         'elevation': {'path': f'{nss}elevation', 'type': 'numeric'}},
        nss=nss)
    sm = SolarMask(data=data)
    return sm


def _parse_spectral_albedo(sa_elements, nss=''):
    if sa_elements is None:
        return []

    from snowprofile.classes import SpectralAlbedo

    r = []
    for e in sa_elements:
        data = _parse_generic_profile(
            e.findall(f'{nss}spectralAlbedoMeasurement'),
            {'min_wavelength': {'path': f'{nss}minWaveLength', 'type': 'numeric'},
             'max_wavelength': {'path': f'{nss}minWaveLength', 'type': 'numeric'},
             'albedo': {'path': f'{nss}albedo', 'type': 'numeric'},
             'uncertainty': {'path': f'{nss}albedo', 'type': 'numeric', 'attribute': '{nss}uncertainty'},
             'quality': {'path': f'{nss}albedo', 'type': 'str', 'attribute': '{nss}quality'},
             },
            nss=nss)
        sm = SpectralAlbedo(data=data)
        r.append(sm)
    return r


def _parse_generic_profile(elements, definitions, nss=''):
    # Eventully get the height to invert depth and height !!
    if elements is None or len(elements) == 0:
        return None
    results = {}
    for key in definitions:
        results[key] = []

    for e in elements:
        for key, value in definitions.items():
            if 'type' in value and value['type'] == 'numeric':
                factor = value['numeric_factor'] if 'numeric_factor' in value else 1
                attribute = value['attribute'] if 'attribute' in value else None
                r = _parse_numeric(e, value['path'], factor=factor, attribute=attribute)
                if 'adapt_total_depth' in value:
                    r = value['adapt_total_depth'] - r
            elif 'type' in value and value['type'] == 'numeric_list':
                factor = value['numeric_factor'] if 'numeric_factor' in value else 1
                attribute = value['attribute'] if 'attribute' in value else None
                r = _parse_numeric_list(e, value['path'], factor=factor, attribute=attribute)
            else:
                attribute = value['attribute'] if 'attribute' in value else None
                r = _parse_str(e, value['path'], attribute=attribute)
            results[key].append(r)

    # Get rid of columns full of None
    results = {key: value for key, value in results.items() if set(value) != set([None])}

    return results


def _parse_stratigraphy(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return None

    if len(nss) > 2:
        ns = nss[1:-1]
    # Metadata key
    mdk = f'{nss}stratMetaData'

    r = []

    for elem in elements:
        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            profile_depth = profile_depth_local
        if profile_depth is None:
            profile_depth = 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'grain_1': {'path': f'{nss}grainFormPrimary', 'type': 'str'},
             'grain_2': {'path': f'{nss}grainFormSecondary', 'type': 'str'},
             'grain_size': {'path': f'{nss}grainSize/{nss}Components/{nss}avg', 'type': 'numeric',
                            'numeric_factor': 0.001},  # mm -> m
             'grain_size_max': {'path': f'{nss}grainSize/{nss}Components/{nss}avgMax', 'type': 'numeric',
                                'numeric_factor': 0.001},
             'hardness': {'path': f'{nss}hardness', 'type': 'str'},
             'wetness': {'path': f'{nss}wetness', 'type': 'str'},
             'loc': {'path': f'{nss}layerOfConcern', 'type': 'str'},
             'comment': {'path': f'{nss}metaData/{nss}comment', 'type': 'str'},
             'formation_time': {'path': f'{nss}validFormationTime/{nss}TimeInstant/{nss}timePosition', 'type': 'str'},
             'formation_period_begin': {'path': f'{nss}validFormationTime/{nss}TimePeriod/{nss}beginPosition',
                                        'type': 'str'},
             'formation_period_end': {'path': f'{nss}validFormationTime/{nss}TimePeriod/{nss}endPosition',
                                      'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import Stratigraphy
        s = Stratigraphy(
            id=_search_gml_id(elem),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData'), namespace=ns),
            data = data)
        r.append(s)

    return r[0] if len(r) > 0 else None


def _parse_temperature_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    if len(nss) > 2:
        ns = nss[1:-1]
    # Metadata key
    mdk = f'{nss}tempMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            profile_depth = profile_depth_local
        if profile_depth is None:
            profile_depth = 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Obs'),
            {'height': {'path': f'{nss}depth', 'type': 'numeric',
                        'numeric_factor': 0.01, 'adapt_total_depth': profile_depth},
             'temperature': {'path': f'{nss}snowTemp', 'type': 'numeric'},
             'uncertainty': {'path': f'{nss}uncertaintyOfMeas', 'type': 'str'},
             'quality': {'path': f'{nss}qualityOfMeas', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import TemperatureProfile
        s = TemperatureProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{nss}tempMetaData/{nss}uncertaintyOfMeas'),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData'), namespace=ns),
            data = data)
        r.append(s)

    return r


def _parse_density_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    if len(nss) > 2:
        ns = nss[1:-1]
    # Metadata key
    mdk = f'{nss}densityMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            profile_depth = profile_depth_local
        if profile_depth is None:
            profile_depth = 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'density': {'path': f'{nss}density', 'type': 'numeric'},
             'uncertainty': {'path': f'{nss}density', 'attribute': 'uncertainty', 'type': 'str'},
             'quality': {'path': f'{nss}density', 'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import DensityProfile
        s = DensityProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            probed_volume = _parse_numeric(elem, f'{mdk}/{nss}probeVolume', factor=1e-6),
            probed_diameter = _parse_numeric(elem, f'{mdk}/{nss}probeDiameter', factor=0.01),
            probed_length = _parse_numeric(elem, f'{mdk}/{nss}probeLength', factor=0.01),
            probed_thickness = _parse_numeric(elem, f'{mdk}/{nss}probedThickness', factor=0.01),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData'), namespace=ns),
            data = data)
        r.append(s)

    return r


def _parse_lwc_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    if len(nss) > 2:
        ns = nss[1:-1]
    # Metadata key
    mdk = f'{nss}lwcMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            profile_depth = profile_depth_local
        if profile_depth is None:
            profile_depth = 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'lwc': {'path': f'{nss}lwc', 'type': 'numeric'},
             'uncertainty': {'path': f'{nss}lwc', 'attribute': 'uncertainty', 'type': 'str'},
             'quality': {'path': f'{nss}lwc', 'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import LWCProfile
        s = LWCProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            probed_thickness = _parse_numeric(elem, f'{mdk}/{nss}probedThickness', factor=0.01),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData'), namespace=ns),
            data = data)
        r.append(s)

    return r


def _parse_ssa_profiles(elements, nss='', profile_depth=0):
    # TODO: To be done, there is Point or Layer profiles !
    # Some post-processing are needed here !
    return []


def _parse_hardness_profiles(elements, nss='', profile_depth=0):
    # TODO: Hardness or RamSonde profile !
    # Some post-processing are needed here !
    return []


def _parse_strength_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    if len(nss) > 2:
        ns = nss[1:-1]
    # Metadata key
    mdk = f'{nss}strengthMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            profile_depth = profile_depth_local
        if profile_depth is None:
            profile_depth = 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'strength': {'path': f'{nss}strengthValue', 'type': 'numeric'},
             'fracture_character': {'path': f'{nss}fractureCharacter', 'type': 'str'},
             'uncertainty': {'path': f'{nss}strengthValue', 'attribute': 'uncertainty', 'type': 'str'},
             'quality': {'path': f'{nss}strengthValue', 'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import StrengthProfile
        s = StrengthProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            probed_area = _parse_numeric(elem, f'{mdk}/{nss}probedArea', factor=1e-4),
            strength_type = _parse_str(elem, f'{mdk}/{nss}strengthType'),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData'), namespace=ns),
            data = data)
        r.append(s)

    return r


def _parse_impurity_profiles(elements, nss='', profile_depth=0):
    # TODO: Be careful, the unit is not specified for mass_fraction and volume_fraction !
    if elements is None or len(elements) == 0:
        return []

    if len(nss) > 2:
        ns = nss[1:-1]
    # Metadata key
    mdk = f'{nss}impurityMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            profile_depth = profile_depth_local
        if profile_depth is None:
            profile_depth = 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'mass_fraction': {'path': f'{nss}massFraction', 'type': 'numeric'},
             'volume_fraction': {'path': f'{nss}volumeFraction', 'type': 'numeric'},
             'uncertainty': {'path': [f'{nss}volumeFraction', f'{nss}massFraction'],
                             'attribute': 'uncertainty', 'type': 'str'},
             'quality': {'path': [f'{nss}volumeFraction', f'{nss}massFraction'],
                         'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import ImpurityProfile
        s = ImpurityProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            impurity_type = _parse_str(elem, f'{mdk}/{nss}impurity'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            probed_volume = _parse_numeric(elem, f'{mdk}/{nss}probeVolume', factor=1e-6),
            probed_diameter = _parse_numeric(elem, f'{mdk}/{nss}probeDiameter', factor=0.01),
            probed_length = _parse_numeric(elem, f'{mdk}/{nss}probeLength', factor=0.01),
            probed_thickness = _parse_numeric(elem, f'{mdk}/{nss}probedThickness', factor=0.01),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData'), namespace=ns),
            data = data)
        r.append(s)

    return r


def _parse_other_scalar_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    if len(nss) > 2:
        ns = nss[1:-1]
    # Metadata key
    mdk = f'{nss}otherScalarMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            profile_depth = profile_depth_local
        if profile_depth is None:
            profile_depth = 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'data': {'path': f'{nss}value', 'type': 'numeric'},
             'uncertainty': {'path': f'{nss}value', 'attribute': 'uncertainty',
                             'type': 'str'},
             'quality': {'path': f'{nss}value', 'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import ScalarProfile
        s = ScalarProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            parameter = _parse_str(elem, f'{mdk}/{nss}parameter'),
            unit = _parse_str(elem, f'{mdk}/{nss}uom'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData'), namespace=ns),
            data = data)
        r.append(s)

    return r


def _parse_other_vectorial_profiles(elements, nss='', profile_depth=0):
    if elements is None or len(elements) == 0:
        return []

    if len(nss) > 2:
        ns = nss[1:-1]
    # Metadata key
    mdk = f'{nss}otherVectorialMetaData'

    r = []

    for elem in elements:
        # Metadata

        # Get the profile depth
        profile_depth_local = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}height',
                                             factor=0.01)  # cm -> m
        if profile_depth_local is not None:
            profile_depth = profile_depth_local
        if profile_depth is None:
            profile_depth = 0

        data = _parse_generic_profile(
            elem.findall(f'{nss}Layer'),
            {'top_height': {'path': f'{nss}depthTop', 'type': 'numeric',
                            'numeric_factor': 0.01, 'adapt_total_depth': profile_depth},
             'thickness': {'path': f'{nss}thickness', 'type': 'numeric',
                           'numeric_factor': 0.01},  # cm -> m
             'data': {'path': f'{nss}value', 'type': 'numeric_list'},
             'uncertainty': {'path': f'{nss}value', 'attribute': 'uncertainty',
                             'type': 'str'},
             'quality': {'path': f'{nss}value', 'attribute': 'quality', 'type': 'str'}},
            nss=nss)

        from snowprofile.profiles import VectorialProfile
        s = VectorialProfile(
            id=_search_gml_id(elem),
            profile_nr = _parse_numeric(elem, path=f'{nss}profileNr'),
            name = _parse_str(elem, path='.', attribute='name'),
            related_profiles = _parse_list(elem, '.', attribute='relatedProfiles'),
            comment = _parse_str(elem, f'{mdk}/{nss}comment'),
            parameter = _parse_str(elem, f'{mdk}/{nss}parameter'),
            unit = _parse_str(elem, f'{mdk}/{nss}uom'),
            rank = _parse_numeric(elem, f'{mdk}/{nss}rank'),
            method_of_measurement = _parse_str(elem, f'{mdk}/{nss}methodOfMeas'),
            quality_of_measurement = _parse_str(elem, f'{mdk}/{nss}qualityOfMeas'),
            uncertainty_of_measurement = _parse_numeric(elem, f'{mdk}/{nss}uncertaintyOfMeas'),
            record_time = _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimeInstant/{nss}timePosition'),
            record_period = (
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}beginPosition'),
                _parse_str(elem, f'{mdk}/{nss}recordTime/{nss}TimePnstant/{nss}endPosition')),
            profile_depth = profile_depth_local,
            profile_swe = _parse_numeric(elem, f'{mdk}/{nss}hS/{nss}Components/{nss}waterEquivalent'),
            additional_data = _parse_additional_data(elem.find(f'{nss}customData'), namespace=ns),
            data = data)
        r.append(s)

    return r


def _parse_stability_tests(elements, nss='', profile_depth=0):
    return []
