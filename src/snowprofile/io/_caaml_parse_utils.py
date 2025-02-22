# -*- coding: utf-8 -*-

import re
import logging
import xml.etree.ElementTree as ET


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


def _parse_additional_data(ad_element, origin='caamlxml6'):
    if ad_element is not None:
        data = ''
        for e in ad_element:
            data += ET.tostring(e, encoding='utf-8').decode('utf-8')
        return {'data': data, 'origin': origin}
    return None
