#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
f = open('./examples/mult.ls8','r')

cpu = CPU()

cpu.load(f.readlines())
cpu.run()