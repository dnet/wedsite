#!/usr/bin/env python

import os, sys

workspace = os.path.dirname(__file__)
sys.path.append(workspace)
os.chdir(workspace)

from wedsite import app as application
