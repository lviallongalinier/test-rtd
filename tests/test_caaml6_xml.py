#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os.path

import snowprofile

_here = os.path.dirname(os.path.realpath(__file__))


class TestCAAML6XML:

    def test_parse_example_file(self):
        """
        Test the parsing of the example file provided on caaml.org on jan. 2025.
        """
        filepath = os.path.join(_here, 'resources/SnowProfile_IACS_SLF22950.xml')
        sp = snowprofile.io.read_caaml6_xml(filepath)

        assert sp.observer.source_name == 'WSL Insitute for Snow and Avalanche Research SLF'
        assert sp.profile_depth == 1.831
        assert len(sp.temperature_profiles) == 1
        assert len(sp.density_profiles) == 1
        assert len(sp.impurity_profiles) == 1
        assert sp.impurity_profiles[0].impurity_type == 'Black Carbon'


if __name__ == "__main__":
    unittest.main()
