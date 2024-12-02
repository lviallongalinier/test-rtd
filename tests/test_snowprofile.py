#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import snowprofile


class TestSnowProfile(unittest.TestCase):
    def test_init_void_snowprofile(self):
        sp = snowprofile.SnowProfile()
        assert sp.id is None


if __name__ == "__main__":
    unittest.main()
