#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import unittest
import tempfile

import snowprofile

_here = os.path.dirname(os.path.realpath(__file__))


class TestIOCAAML6XML(unittest.TestCase):

    def test_read_caaml6_xml_default_example(self):
        sp = snowprofile.io.read_caaml6_xml(os.path.join(_here, 'resources', 'SnowProfile_IACS_SLF22950.xml'))

        assert sp.observer.source_name == 'WSL Insitute for Snow and Avalanche Research SLF'
        assert sp.location.name == 'Chörbschhorn - Hanengretji - Davos'
        assert sp.application == 'SnowProfiler'
        assert sp.weather.cloudiness == 'FEW'

    def test_read_write_caaml6_xml_example2(self):
        sp = snowprofile.io.read_caaml6_xml(os.path.join(_here, 'resources', 'TestProfile2.caaml'))

        with tempfile.TemporaryDirectory(prefix='snowprofiletests') as dirname:
            filename = os.path.join(dirname, 'testcaaml.caaml')
            snowprofile.io.write_caaml6_xml(sp, filename)
            sp_reread = snowprofile.io.read_caaml6_xml(filename)

        assert snowprofile.io.to_json(sp) == snowprofile.io.to_json(sp_reread)


if __name__ == "__main__":
    unittest.main()
