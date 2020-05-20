#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# sys.argv[0] == "ls8.py"
# sys.argv[1] == "examples/mult.ls8"

cpu.load()
cpu.run()
