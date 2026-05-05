#!/usr/bin/env python.sh
#
# test0.py
#
# Test for standalone Isaac Sim

from isaacsim.simulation_app import SimulationApp

simulation_app = SimulationApp({"headless": True})

from isaacsim.core.version import get_version

print("Isaac Sim version: ", get_version())
