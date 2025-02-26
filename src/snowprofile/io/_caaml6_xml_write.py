# -*- coding: utf-8 -*-

import logging
import datetime
import xml.etree.ElementTree as ET

import numpy as np

# Note to developpers:
# XML elements are prefixed by e_
# Snowprofile data is prefixes by s_

table_versions_uri = {
    '6.0.6': 'http://caaml.org/Schemas/SnowProfileIACS/v6.0.6',
    '6.0.5': 'http://caaml.org/Schemas/SnowProfileIACS/v6.0.5'}

uri_gml = 'http://www.opengis.net/gml'


def write_caaml6_xml(snowprofile, filename, version='6.0.5'):
    """
    Write a SnowProfile object into a CAAML 6 XML-based IACS Snow Profile document.

    Currently supported versions:

    - 6.0.6
    - 6.0.5 (default)

    :param snowprofile: A SnowProfile object to dump to a CAAML file
    :type snowprofile: SnowProfile
    :param filename: The filename to write into. If already exists, will be overwritten.
    :type filename: str
    """
    if version not in table_versions_uri:
        raise ValueError(f'Unsupported CAAML version {version}.')
    uri = table_versions_uri[version]
    ns = '{' + uri + '}'
    ns_gml = '{' + uri_gml + '}'

    # Namespaces
    ET.register_namespace('caaml', uri)
    ET.register_namespace('gml', uri_gml)

    # Id management
    id_list = []

    def _gen_id(id, default=None):
        if id is None and default is not None:
            return _gen_id(default)
        elif id is None and default is None:
            return _gen_id('id')
        else:
            i = 1
            id_test = id
            while id_test in id_list:
                id_test = f'{id}{i}'
                i += 1
            id = id_test
            id_list.append(id)
            return id

    config = {'_gen_id': _gen_id,
              'ns': ns,
              'ns_gml': ns_gml,
              'profile_depth': snowprofile.profile_depth if snowprofile.profile_depth is not None else 0,
              'profile_swe': snowprofile.profile_swe,
              'version': version}

    # Main XML element
    root = ET.Element(f'{ns}SnowProfile', attrib={f'{ns_gml}id': _gen_id(snowprofile.id, 'snowprofile')})

    # - Metadata (optional)
    if snowprofile.comment is not None:
        _ = ET.SubElement(root, f'{ns}metaData')
        _ = ET.SubElement(_, f'{ns}comment')
        _.text = snowprofile.comment

    # - timeRef
    time = ET.SubElement(root, f'{ns}timeRef')
    record_time = ET.SubElement(time, f'{ns}recordTime')
    if snowprofile.time.record_period[0] is not None and snowprofile.time.record_period[1] is not None:
        _ = ET.SubElement(record_time, f'{ns}TimePeriod')
        begin = ET.SubElement(_, f'{ns}beginPosition')
        begin.text = snowprofile.time.record_period[0].isoformat()
        end = ET.SubElement(_, f'{ns}endPosition')
        end.text = snowprofile.time.record_period[1].isoformat()
    elif snowprofile.time.record_time is not None:
        _ = ET.SubElement(record_time, f'{ns}TimeInstant')
        begin = ET.SubElement(_, f'{ns}timePosition')
        begin.text = snowprofile.time.record_time.isoformat()
    else:
        logging.error('Could not find a valid record time or time period. Use current time')
        _ = ET.SubElement(record_time, f'{ns}TimeInstant')
        begin = ET.SubElement(_, f'{ns}timePosition')
        begin.text = datetime.datetime.now().isoformat()

    if snowprofile.time.report_time is not None:
        _ = ET.SubElement(root, f'{ns}dateTimeReport')
        _.text = snowprofile.time.report_time.isoformat()

    if snowprofile.time.last_edition_time is not None:
        _ = ET.SubElement(root, f'{ns}dateTimeLastEdit')
        _.text = snowprofile.time.last_edition_time.isoformat()

    if snowprofile.time.comment is not None:
        _ = ET.SubElement(time, f'{ns}metaData')
        _ = ET.SubElement(_, f'{ns}comment')
        _.text = snowprofile.time.comment

    _append_additional_data(root, snowprofile.time.additional_data, ns=ns)

    # - srcRef
    src = ET.SubElement(root, f'{ns}srcRef')
    if snowprofile.observer.source_name is None:
        src = ET.SubElement(src, f'{ns}Person',
                            attrib={f'{ns_gml}id': _gen_id(snowprofile.observer.contact_persons[0].id, 'person')})
        if len(snowprofile.observer.contact_persons) > 1:
            logging.error('Observer: if you provide more than one contact person you need to provide a source name. '
                          'Only the first contact person will be used.')
        _ = ET.SubElement(src, f'{ns}name')
        _.text = snowprofile.observer.contact_persons[0].name
        if snowprofile.observer.contact_persons[0].comment is not None:
            _ = ET.SubElement(src, f'{ns}metaData')
            _ = ET.SubElement(_, f'{ns}comment')
            _.text = snowprofile.observer.contact_persons[0].comment
        _append_additional_data(src, snowprofile.observer.contact_persons[0].additional_data, ns=ns)
    else:
        op = ET.SubElement(src, f'{ns}Operation', attrib={f'{ns_gml}id': _gen_id(snowprofile.observer.source_id,
                                                                                 'operation')})
        _ = ET.SubElement(op, f'{ns}name')
        _.text = snowprofile.observer.source_name
        _append_additional_data(op, snowprofile.observer.source_additional_data, ns=ns)
        if snowprofile.observer.source_comment is not None:
            _ = ET.SubElement(op, f'{ns}metaData')
            _ = ET.SubElement(_, f'{ns}comment')
            _.text = snowprofile.observer.source_comment
        for person in snowprofile.observer.contact_persons:
            p = ET.SubElement(op, f'{ns}contactPerson', attrib={f'{ns_gml}id': _gen_id(person.id, 'person')})
            name = ET.SubElement(p, f'{ns}name')
            name.text = person.name
            _append_additional_data(p, person.additional_data, ns=ns)
            if person.comment is not None:
                _ = ET.SubElement(p, f'{ns}metaData')
                _ = ET.SubElement(_, f'{ns}comment')
                _.text = person.comment

    # locRef
    src = ET.SubElement(root, f'{ns}locRef', attrib={f'{ns_gml}id': _gen_id(snowprofile.location.id, 'location')})
    loc = snowprofile.location
    if loc.comment is not None:
        _ = ET.SubElement(src, f'{ns}metaData')
        _ = ET.SubElement(_, f'{ns}comment')
        _.text = loc.comment
    name = ET.SubElement(src, f'{ns}name')
    name.text = loc.name
    if loc.point_type is not None:
        _ = ET.SubElement(src, f'{ns}obsPointSubType')
        _.text = loc.point_type
    if loc.elevation is not None:
        _ = ET.SubElement(src, f'{ns}validElevation')
        _ = ET.SubElement(_, f'{ns}ElevationPosition', attrib={'uom': 'm'})
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(int(loc.elevation))
    if loc.aspect is not None:
        _ = ET.SubElement(src, f'{ns}validAspect')
        _ = ET.SubElement(_, f'{ns}AspectPosition')
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(int(loc.aspect))
    if loc.slope is not None:
        _ = ET.SubElement(src, f'{ns}validSlopeAngle')
        _ = ET.SubElement(_, f'{ns}SlopeAnglePosition', attrib={'uom': 'deg'})
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(int(loc.slope))
    _ = ET.SubElement(src, f'{ns}pointLocation')
    _ = ET.SubElement(_, f'{ns_gml}Point', attrib={f'{ns_gml}id': _gen_id('pointID'),
                                                   'srsName': "urn:ogc:def:crs:OGC:1.3:CRS84",
                                                   'srsDimension': "2"})
    _ = ET.SubElement(_, f'{ns_gml}pos')
    _.text = f'{loc.latitude} {loc.longitude}'
    if loc.country is not None:
        _ = ET.SubElement(src, f'{ns}country')
        _.text = loc.country
    if loc.region is not None:
        _ = ET.SubElement(src, f'{ns}region')
        _.text = loc.region
    _append_additional_data(src, loc.additional_data, ns=ns)

    # application  and application_version (optional)
    if snowprofile.application is not None:
        _ = ET.SubElement(root, f'{ns}application')
        _.text = snowprofile.application
    if snowprofile.application_version is not None:
        _ = ET.SubElement(root, f'{ns}applicationVersion')
        _.text = snowprofile.application_version

    _append_additional_data(root, snowprofile.additional_data, ns=ns)

    # snowProfileResultsOf
    e_r = ET.SubElement(root, f'{ns}snowProfileResultsOf')
    e_r = ET.SubElement(e_r, f'{ns}SnowProfileMeasurements', attrib={f'{ns}dir': 'top down'})

    if snowprofile.profile_comment is not None:
        _ = ET.SubElement(e_r, f'{ns}metaData')
        _ = ET.SubElement(_, f'{ns}comment')
        _.text = snowprofile.profile_comment

    # profileDepth seem to be designed to be the observed depth rather than the total depth
    # if snowprofile.profile_depth is not None:
    #     _ = ET.SubElement(r, f'{ns}profileDepth', attrib={'uom': 'cm'})
    #     _.text = str(float(snowprofile.profile_depth) * 100)

    # - Weather
    e_weather = ET.SubElement(e_r, f'{ns}weathercond')
    s_weather = snowprofile.weather

    e_weather_metadata = ET.SubElement(e_weather, f'{ns}metaData')
    comment = ''
    if s_weather.air_temperature_measurement_height is not None and version >= "6.0.6":
        _ = ET.SubElement(e_weather_metadata, f'{ns}airTempMeasurementHeight')
        _.text = snowprofile.profile_comment
    elif s_weather.air_temperature_measurement_height is not None:
        comment += f'Height of the temperature measurement: {s_weather.air_temperature_measurement_height}m'
    if s_weather.wind_measurement_height is not None and version >= "6.0.6":
        _ = ET.SubElement(e_weather_metadata, f'{ns}airTempMeasurementHeight')
        _.text = snowprofile.profile_comment
    elif s_weather.wind_measurement_height is not None:
        comment += f'Height of the wind measurement: {s_weather.wind_measurement_height}m'
    if s_weather.comment is not None or len(comment) > 1:
        if s_weather.comment is not None and len(comment) == 0:
            comment = s_weather.comment
        else:
            comment = s_weather.comment + "\n\n" + comment
        _ = ET.SubElement(e_weather_metadata, f'{ns}comment')
        _.text = comment

    if s_weather.cloudiness is not None:
        _ = ET.SubElement(e_weather, f'{ns}skyCond')
        _.text = s_weather.cloudiness
    if s_weather.precipitation is not None:
        _ = ET.SubElement(e_weather, f'{ns}precipTI')
        _.text = s_weather.precipitation
    if s_weather.air_temperature is not None:
        _ = ET.SubElement(e_weather, f'{ns}airTempPres', attrib={'uom': 'degC'})
        _.text = str(s_weather.air_temperature)
    if s_weather.wind_speed is not None:
        _ = ET.SubElement(e_weather, f'{ns}windSpd', attrib={'uom': 'ms-1'})
        _.text = str(s_weather.wind_speed)
    if s_weather.wind_direction is not None:
        _ = ET.SubElement(e_weather, f'{ns}windDir')
        _ = ET.SubElement(_, f'{ns}AspectPosition')
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(int(s_weather.wind_speed))
    _append_additional_data(e_weather, s_weather.additional_data, ns=ns)

    # - Snowpack
    e_snowpack = ET.SubElement(e_r, f'{ns}snowPackCond')
    if snowprofile.profile_depth is not None or snowprofile.profile_swe is not None:
        hs = ET.SubElement(e_snowpack, f'{ns}hS')
        hsc = ET.SubElement(hs, f'{ns}Components')
        if snowprofile.profile_depth is not None:
            _ = ET.SubElement(hsc, f'{ns}height', attrib={'uom': 'cm'})
            _.text = str(snowprofile.profile_depth * 100)
        if snowprofile.profile_swe is not None:
            _ = ET.SubElement(hsc, f'{ns}waterEquivalent', attrib={'uom': 'kgm-2'})
            _.text = str(snowprofile.profile_swe)
    if (snowprofile.profile_depth_std is not None or snowprofile.profile_swe_std is not None):
        if version >= "6.0.6":
            hs = ET.SubElement(e_snowpack, f'{ns}hSVariability')
            hsc = ET.SubElement(hs, f'{ns}Components')
            if snowprofile.profile_depth_std is not None:
                _ = ET.SubElement(hsc, f'{ns}height', attrib={'uom': 'cm'})
                _.text = str(snowprofile.profile_depth_std * 100)
            if snowprofile.profile_swe_std is not None:
                _ = ET.SubElement(hsc, f'{ns}waterEquivalent', attrib={'uom': 'kgm-2'})
                _.text = str(snowprofile.profile_swe_std)
        else:
            logging.warning('Caaml 6 < 6.0.6 does not support profile_depth_std and profile_swe_std.')
    if snowprofile.new_snow_24_depth is not None or snowprofile.new_snow_24_swe is not None:
        hs = ET.SubElement(e_snowpack, f'{ns}hN24')
        hsc = ET.SubElement(hs, f'{ns}Components')
        if snowprofile.new_snow_24_depth is not None:
            _ = ET.SubElement(hsc, f'{ns}height', attrib={'uom': 'cm'})
            _.text = str(snowprofile.new_snow_24_depth * 100)
        if snowprofile.new_snow_24_swe is not None:
            _ = ET.SubElement(hsc, f'{ns}waterEquivalent', attrib={'uom': 'kgm-2'})
            _.text = str(snowprofile.new_snow_24_swe)
    if (snowprofile.new_snow_24_depth_std is not None or snowprofile.new_snow_24_swe_std is not None):
        hs = ET.SubElement(e_snowpack, f'{ns}hIN')
        hsc = ET.SubElement(hs, f'{ns}Components')
        if snowprofile.new_snow_24_depth_std is not None:
            _ = ET.SubElement(hsc, f'{ns}height', attrib={'uom': 'cm'})
            _.text = str(snowprofile.new_snow_24_depth_std * 100)
        if snowprofile.new_snow_24_swe_std is not None:
            _ = ET.SubElement(hsc, f'{ns}waterEquivalent', attrib={'uom': 'kgm-2'})
            _.text = str(snowprofile.new_snow_24_swe_std)
    if snowprofile.snow_transport is not None:
        if version >= "6.0.6":
            _ = ET.SubElement(e_snowpack, f'{ns}snowTransport')
            _.text = snowprofile.snow_transport
        else:
            logging.warning('Caaml 6 < 6.0.6 does not support snow transport data.')
    if snowprofile.snow_transport_occurence_24 is not None:
        if version >= "6.0.6":
            _ = ET.SubElement(e_snowpack, f'{ns}snowTransportOccurence24')
            _.text = str(snowprofile.snow_transport_occurence_24)
        else:
            logging.warning('Caaml 6 < 6.0.6 does not support snow transport data.')

    #  - Surface characterization
    e_surf = ET.SubElement(e_r, f'{ns}surfCond')
    s_surf = snowprofile.surface_conditions
    comment = ''
    if s_surf.comment is not None:
        _ = ET.SubElement(e_surf, f'{ns}metaData')
        _ = ET.SubElement(_, f'{ns}comment')
        _.text = s_surf.comment
    if s_surf.penetration_ram is not None:
        _ = ET.SubElement(e_surf, f'{ns}penetrationRam', attrib={'uom': 'cm'})
        _.text = str(float(s_surf.penetration_ram) * 100)
    if s_surf.penetration_foot is not None:
        _ = ET.SubElement(e_surf, f'{ns}penetrationFoot', attrib={'uom': 'cm'})
        _.text = str(float(s_surf.penetration_foot) * 100)
    if s_surf.penetration_ski is not None:
        _ = ET.SubElement(e_surf, f'{ns}penetrationSki', attrib={'uom': 'cm'})
        _.text = str(float(s_surf.penetration_ski) * 100)

    _ = ET.SubElement(e_surf, f'{ns}surfFeatures')
    e_surff = ET.SubElement(_, f'{ns}Components')
    _ = ET.SubElement(e_surff, f'{ns}surfRoughness')
    if s_surf.surface_roughness is not None:
        _.text = s_surf.surface_roughness
    else:
        _.text = 'unknown'
    if s_surf.surface_wind_features is not None:
        if version >= "6.0.6":
            _ = ET.SubElement(e_surff, f'{ns}surfWindFeatures')
            _.text = s_surf.surface_wind_features
        else:
            comment += f'Wind surface features: {s_surf.surface_wind_features}\n'
    if s_surf.surface_melt_rain_features is not None:
        if version >= "6.0.6":
            _ = ET.SubElement(e_surff, f'{ns}surfMeltRainFeatures')
            _.text = s_surf.surface_melt_rain_features
        else:
            comment += f'Melt and rain surface features: {s_surf.surface_melt_rain_features}\n'

    if s_surf.surface_features_amplitude is not None:
        if s_surf.surface_features_amplitude_min is not None or s_surf.surface_features_amplitude_max is not None:
            logging.warning('CAAML6 could not store both surface_feature amplitude and min/max of amplitude.')
        _ = ET.SubElement(e_surff, f'{ns}validAmplitude')
        _ = ET.SubElement(_, f'{ns}AmplitudePosition', attrib={'uom': 'cm'})
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(float(s_surf.surface_features_amplitude) * 100)
    elif s_surf.surface_features_amplitude_min is not None and s_surf.surface_features_amplitude_max is not None:
        _ = ET.SubElement(e_surff, f'{ns}validAmplitude')
        _r = ET.SubElement(_, f'{ns}AmplitudeRange', attrib={'uom': 'cm'})
        _ = ET.SubElement(_r, f'{ns}beginPosition')
        _.text = str(float(s_surf.surface_features_amplitude_min) * 100)
        _ = ET.SubElement(_r, f'{ns}endPosition')
        _.text = str(float(s_surf.surface_features_amplitude_max) * 100)

    if s_surf.surface_features_wavelength is not None:
        if s_surf.surface_features_wavelength_min is not None or s_surf.surface_features_wavelength_max is not None:
            logging.warning('CAAML6 could not store both surface_feature wavelength and min/max of wavelength.')
        _ = ET.SubElement(e_surff, f'{ns}validWavelength')
        _ = ET.SubElement(_, f'{ns}WavelengthPosition', attrib={'uom': 'm'})
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(float(s_surf.surface_features_wavelength))
    elif s_surf.surface_features_wavelength_min is not None and s_surf.surface_features_wavelength_max is not None:
        _ = ET.SubElement(e_surff, f'{ns}validWavelength')
        _r = ET.SubElement(_, f'{ns}WavelengthRange', attrib={'uom': 'm'})
        _ = ET.SubElement(_r, f'{ns}beginPosition')
        _.text = str(float(s_surf.surface_features_wavelength_min))
        _ = ET.SubElement(_r, f'{ns}endPosition')
        _.text = str(float(s_surf.surface_features_wavelength_max))

    if s_surf.surface_features_aspect is not None:
        _ = ET.SubElement(e_surff, f'{ns}validAspect')
        _ = ET.SubElement(_, f'{ns}AspectPosition')
        _ = ET.SubElement(_, f'{ns}position')
        _.text = str(int(s_surf.surface_features_aspect))

    if version >= "6.0.6":
        _ = ET.SubElement(e_surff, f'{ns}lapPresence')
        if s_surf.lap_presence is None:
            _.text = 'unknown'
        else:
            _.text = s_surf.lap_presence

        if s_surf.surface_temperature is not None:
            _surftemp = ET.SubElement(e_surff, f'{ns}surfTemp')
            if s_surf.surface_temperature_measurement_method is not None:
                _ = ET.SubElement(_surftemp, f'{ns}methodOfMeas')
                _.text = s_surf.surface_temperature_measurement_method
            _ = ET.SubElement(_surftemp, f'{ns}data', attrib={'uom': 'degC'})
            _.text = str(s_surf.surface_temperature)
    else:
        if s_surf.lap_presence is not None:
            comment += f'LAP presence: {s_surf.lap_presence}\n'
        if s_surf.surface_temperature is not None:
            comment += f'Surface temperature: {s_surf.surface_temperature}\n'
        if s_surf.surface_temperature_measurement_method is not None:
            comment += f'Surface temperature measurement method: {s_surf.surface_temperature_measurement_method}\n'

    if s_surf.surface_albedo is not None or s_surf.spectral_albedo is not None:
        logging.warning('Surface and spectral albedo not yet implemented for CAAML6 output')
        # TODO: To be implemented.

    if s_surf.comment is not None or len(comment) > 0:
        if s_surf.comment is not None and len(comment) == 0:
            comment = s_surf.comment
        elif s_surf.comment is not None:
            comment = s_surf.comment + "\n\n" + comment
        _ = ET.SubElement(e_surf, f'{ns}metaData')
        _ = ET.SubElement(e_surf, f'{ns}comment')
        _.text = comment

    _append_additional_data(e_surf, s_surf.additional_data)

    # - Profiles
    # TODO: tbd  <24-02-25, Léo Viallon-Galinier> #
    _insert_stratigrpahy_profile(e_r, snowprofile.stratigraphy_profile, config=config)

    if version >= "6.0.6":
        for profile in snowprofile.temperature_profiles:
            _insert_temperature_profile(e_r, profile, config=config)
    else:
        if len(snowprofile.temperature_profiles) > 1:
            logging.error(f'Only one temperature profile acepted in CAAML v{version}.')
        if len(snowprofile.temperature_profiles) > 0:
            _insert_temperature_profile(e_r, snowprofile.temperature_profiles[0], config=config)

    for profile in snowprofile.density_profiles:
        _insert_density_profile(e_r, profile, config=config)

    # - Additional data
    _append_additional_data(e_r, snowprofile.profile_additional_data)

    #
    # Generate Tree from mail element and write
    #
    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8',
               xml_declaration=True)


def _append_additional_data(element, data, ns=''):
    if data is None or data.data is None:
        return None
    # TODO: tbd  <24-02-25, Léo Viallon-Galinier> #


def _gen_common_attrib(s, config={}):
    attrib = {}
    ns_gml = config['ns_gml']
    if s.id is not None:
        attrib[f'{ns_gml}id'] = config['_gen_id'](s.id)
    if len(s.related_profiles) > 0:
        attrib['relatedProfiles'] = ' '.join(s.related_profiles)
    if s.name is not None:
        attrib['name'] = ' '.join(s.name)
    return attrib


def _gen_common_metadata(e, s, config={}, additional_metadata = [], name='metaData'):
    """
    Metadata handler common to all profiles.
    Also deal with additional_data
    """
    ns = config['ns']
    comment = ''

    e_md = ET.SubElement(e, f'{ns}{name}')

    e_hs = None
    if s.profile_depth is not None and s.profile_depth != config['profile_depth']:
        if config['version'] >= "6.0.6":
            e_hs = ET.SubElement(e_md, f"{ns}hS")
            e_hs = ET.SubElement(e_hs, f"{ns}Components")
            _ = ET.SubElement(e_hs, f"{ns}height", attrib={'uom': 'cm'})
            _.text = str(s.profile_depth * 100)
        else:
            comment += f"Profile depth: {s.profile_depth}m\n"
    if s.profile_swe is not None and s.profile_swe != config['profile_swe']:
        if config['version'] >= "6.0.6":
            if e_hs is None:
                e_hs = ET.SubElement(e_md, f"{ns}hS")
                e_hs = ET.SubElement(e_hs, f"{ns}Components")
            _ = ET.SubElement(e_hs, f"{ns}waterEquivalent", attrib={'uom': 'kgm-2'})
            _.text = str(s.profile_swe)
        else:
            comment += f"Profile SWE: {s.profile_swe}m\n"

    if s.record_period[0] is not None and s.record_period[1] is not None:
        e_record_time = ET.SubElement(e_md, f'{ns}recordTime')
        _ = ET.SubElement(e_record_time, f'{ns}TimePeriod')
        begin = ET.SubElement(_, f'{ns}beginPosition')
        begin.text = s.record_period[0].isoformat()
        end = ET.SubElement(_, f'{ns}endPosition')
        end.text = s.record_period[1].isoformat()
    elif s.record_time is not None:
        e_record_time = ET.SubElement(e_md, f'{ns}recordTime')
        _ = ET.SubElement(e_record_time, f'{ns}TimeInstant')
        begin = ET.SubElement(_, f'{ns}timePosition')

    for elem in additional_metadata:
        value = elem['value']
        # None values
        if value is None:
            continue
        # Check version
        if 'min_version' in elem and elem['min_version'] < config['version']:
            if 'comment_title' in elem:
                comment += f'{elem["comment_title"]}: {value}'
                continue

        # Get the value and pre-process to get a string
        if 'values' in elem and elem['values'] is not None and value not in elem['values']:
            if 'default_value' in elem:
                value = elem['default_value']
            else:  # Invalid value and no default value
                continue
        if 'factor' in elem:
            value = value * elem['factor']
        if isinstance(value, float):
            value = "{:.12g}".format(value)
        elif not isinstance(value, str):
            value = str(value)

        # Write the metadata
        key = elem['key']
        _ = ET.SubElement(e_md, f'{ns}{key}',
                          attrib=elem['attrib'] if 'attrib' in elem and elem['attrib'] is not None else {})
        _.text = value

    if s.comment is not None or len(comment) > 0:
        if s.comment is not None and len(comment) == 0:
            comment = s.comment
        elif s.comment is not None:
            comment = s.comment + "\n\n" + comment
        _ = ET.SubElement(e_md, f'{ns}comment')
        _.text = comment

    # Additional data
    _append_additional_data(e, s.additional_data, ns=ns)

    return e_md


def _insert_stratigrpahy_profile(e_r, s_strat, config):
    if s_strat is None:
        return

    ns = config['ns']
    profile_depth = config['profile_depth']

    e_s = ET.SubElement(e_r, 'stratProfile',
                        attrib=_gen_common_attrib(s_strat, config=config))
    e_md = _gen_common_metadata(e_s, s_strat, config=config, name='stratMetaData')

    # Layer loop
    for _, layer in s_strat.data.iterrows():
        e_layer = ET.SubElement(e_s, f'{ns}Layer')
        _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
        _.text = "{:.12g}".format((profile_depth - layer.top_height) * 100)
        if not np.isnan(layer.thickness):
            _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
            _.text = "{:.12g}".format(layer.thickness * 100)
        if layer.grain_1 is not None:
            _ = ET.SubElement(e_layer, f'{ns}grainFormPrimary')
            _.text = layer.grain_1
        if layer.grain_1 is not None and layer.grain_2 is not None:
            _ = ET.SubElement(e_layer, f'{ns}grainFormSecondary')
            _.text = layer.grain_2
        if layer.grain_size is not None:
            _ = ET.SubElement(e_layer, f'{ns}grainSize')
            _c = ET.SubElement(_, f'{ns}Components', attrib={'uom': 'mm'})
            _ = ET.SubElement(_c, f'{ns}avg')
            _.text = "{:.12g}".format(layer.grain_size * 1e3)
            if 'grain_size_max' in layer and not np.isnan(layer.grain_size_max):
                _ = ET.SubElement(_c, f'{ns}avgMax')
                _.text = "{:.12g}".format(layer.grain_size_max * 1e3)
        if layer.hardness is not None:
            _ = ET.SubElement(e_layer, f'{ns}hardness', attrib={'uom': ''})
            _.text = layer.hardness
        if layer.wetness is not None:
            _ = ET.SubElement(e_layer, f'{ns}wetness', attrib={'uom': ''})
            _.text = layer.wetness
        if 'loc' in layer and layer.loc is not None:
            _ = ET.SubElement(e_layer, f'{ns}layerOfConcern')
            _.text = layer.loc
        _md = None
        if ('comment' in layer and layer.comment is not None and len(layer.comment) > 0):
            _md = ET.SubElement(e_layer, f'{ns}metaData')
            _ = ET.SubElement(_md, f'{ns}comment')
            _.text = str(layer.comment)
        if 'additional_data' in layer and layer.additional_data is not None:
            if _md is None:
                _md = ET.SubElement(e_layer, f'{ns}metaData')
                _append_additional_data(_md, layer.additional_data, ns=ns)
        if 'formation_time' in layer and layer.formation_time is not None:
            _ = ET.SubElement(e_layer, f'{ns}validFormationTime')
            _t = ET.SubElement(_, f'{ns}TimeInstant')
            _ = ET.SubElement(_t, f'{ns}timePosition')
            _.text = layer.formation_time.isoformat()
        elif ('formation_period_begin' in layer and 'formation_period_end' in layer
              and layer.formation_period_begin is not None and layer.formation_period_end is not None):
            _ = ET.SubElement(e_layer, f'{ns}validFormationTime')
            _t = ET.SubElement(_, f'{ns}TimePeriod')
            _ = ET.SubElement(_t, f'{ns}beginPosition')
            _.text = layer.formation_period_begin.isoformat()
            _ = ET.SubElement(_t, f'{ns}endPosition')
            _.text = layer.formation_period_end.isoformat()


_density_mom = {'6.0.5': ['Snow Tube', 'Snow Cylinder', 'Snow Cutter', 'Denoth Probe', 'other']}


def _insert_density_profile(e_r, s_p, config):
    if s_p is None:
        return

    ns = config['ns']
    profile_depth = config['profile_depth']
    version = config['version']

    e_p = ET.SubElement(e_r, 'densityProfile',
                        attrib=_gen_common_attrib(s_p, config=config))

    if s_p.profile_nr is not None:
        _ = ET.SubElement(e_p, f'{ns}profileNr')
        _.text = str(s_p.profile_nr)

    e_md = _gen_common_metadata(
        e_p, s_p, config=config,
        name = 'densityMetaData',
        additional_metadata = [
            {'value': s_p.method_of_measurement, 'default_value': 'Other',
             'values': _density_mom[version] if version in _density_mom else None,
             'key': 'methodOfMeas'},
            {'value': s_p.quality_of_measurement, 'min_version': '6.0.6', 'comment_title': 'Quality of measurement',
             'key': 'qualityOfMeas'},
            {'value': s_p.uncertainty_of_measurement, 'key': 'uncertaintyOfMeas', 'attrib': {'uom': 'kgm-3'}},
            {'value': s_p.probed_volume, 'key': 'probeVolume', 'factor': 1e6, 'attrib': {'uom': 'cm3'}},
            {'value': s_p.probed_diameter, 'key': 'probeDiameter', 'factor': 100, 'attrib': {'uom': 'cm'}},
            {'value': s_p.probed_length, 'key': 'probeLength', 'factor': 100, 'attrib': {'uom': 'cm'}},
            {'value': s_p.probed_thickness, 'key': 'probeThickness', 'factor': 100, 'attrib': {'uom': 'cm'}}, ])

    # Loop layers
    for _, layer in s_p.data.iterrows():
        e_layer = ET.SubElement(e_p, f'{ns}Layer')
        _ = ET.SubElement(e_layer, f'{ns}depthTop', attrib={'uom': 'cm'})
        _.text = "{:.12g}".format((profile_depth - layer.top_height) * 100)
        if not np.isnan(layer.thickness):
            _ = ET.SubElement(e_layer, f'{ns}thickness', attrib={'uom': 'cm'})
            _.text = "{:.12g}".format(layer.thickness * 100)
        attrib = {'uom': 'kgm-3'}
        if 'uncertainty' in layer and not np.isnan(layer.uncertainty) and version >= '6.0.6':
            attrib['uncertainty'] = "{:.12g}".format(layer.uncertainty)
        if 'quality' in layer and layer.quality is not None and version >= '6.0.6':
            attrib['quality'] = layer.quality
        _ = ET.SubElement(e_layer, f'{ns}density', attrib=attrib)
        _.text = "{:.12g}".format(layer.density)


def _insert_temperature_profile(e_r, s_p, config):
    if s_p is None:
        return

    ns = config['ns']
    profile_depth = config['profile_depth']
    version = config['version']

    e_p = ET.SubElement(e_r, 'tempProfile',
                        attrib=_gen_common_attrib(s_p, config=config))

    if version > "6.0.6" and s_p.profile_nr is not None:
        _ = ET.SubElement(e_p, f'{ns}profileNr')
        _.text = str(s_p.profile_nr)

    e_md = _gen_common_metadata(
        e_p, s_p, config=config,
        name = 'tempMetaData',
        additional_metadata = [
            {'value': s_p.method_of_measurement, 'min_version': '6.0.6', 'comment_title': 'Measurement method',
             'key': 'methodOfMeas'},
            {'value': s_p.quality_of_measurement, 'min_version': '6.0.6', 'comment_title': 'Quality of measurement',
             'key': 'qualityOfMeas'},
            {'value': s_p.uncertainty_of_measurement, 'key': 'uncertaintyOfMeas', 'attrib': {'uom': 'degC'},
             'min_version': '6.0.6', 'comment_title': 'Uncertainty of measurement (degC)'}, ])

    # Loop layers
    for _, layer in s_p.data.iterrows():
        e_layer = ET.SubElement(e_p, f'{ns}Obs')
        _ = ET.SubElement(e_layer, f'{ns}depth', attrib={'uom': 'cm'})
        _.text = "{:.12g}".format((profile_depth - layer.height) * 100)
        _ = ET.SubElement(e_layer, f'{ns}snowTemp', attrib={'uom': 'degC'})
        _.text = "{:.12g}".format(layer.temperature)
        if 'uncertainty' in layer and not np.isnan(layer.uncertainty) and version >= '6.0.6':
            _ = "{:.12g}".format(layer.uncertainty)
        if 'quality' in layer and layer.quality is not None and version >= '6.0.6':
            _ = ET.SubElement(e_layer, f'{ns}qualityOfMeas')
            _.text = layer.quality
