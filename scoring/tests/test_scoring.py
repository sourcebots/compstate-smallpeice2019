#!/usr/bin/env python

import unittest

# Path hackery
import os.path
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)

from score import Scorer, InvalidScoresheetException

TEAMS_DATA =  {
    'ABC': {'zone': 0},  # green
    'DEF': {'zone': 1},  # orange
    'GHI': {'zone': 2},  # purple
}


class ScorerTests(unittest.TestCase):
    longMessage = True


if __name__ == '__main__':
    unittest.main()
