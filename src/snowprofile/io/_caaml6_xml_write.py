# -*- coding: utf-8 -*-

import logging
import datetime
import xml.etree.ElementTree as ET

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
    if snowprofile.time.record_period is not None and snowprofile.time.record_period[0] is not None \
    and snowprofile.time.record_period[1] is not None:
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
    r = ET.SubElement(root, f'{ns}snowProfileResultsOf')
    r = ET.SubElement(r, f'{ns}SnowProfileMeasurements', attrib={f'{ns}dir': 'top down'})

    if snowprofile.profile_comment is not None:
        _ = ET.SubElement(r, f'{ns}metaData')
        _ = ET.SubElement(_, f'{ns}comment')
        _.text = snowprofile.profile_comment

    # profileDepth seem to be designed to be the observed depth rather than the total depth
    # if snowprofile.profile_depth is not None:
    #     _ = ET.SubElement(r, f'{ns}profileDepth', attrib={'uom': 'cm'})
    #     _.text = str(float(snowprofile.profile_depth) * 100)

    # - Weather
    e_weather = ET.SubElement(r, f'{ns}weathercond')
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
    e_snowpack = ET.SubElement(r, f'{ns}snowPackCond')
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
    e_surf = ET.SubElement(r, f'{ns}surfCond')
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

    # - Additional data
    _append_additional_data(r, snowprofile.profile_additional_data)

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
