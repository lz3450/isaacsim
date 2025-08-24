#!/usr/bin/env python.sh
#
# test1.py
#
# Test for standalone Isaac Sim extension loading
#

from isaacsim.simulation_app import SimulationApp

simulation_app = SimulationApp({"headless": False})

from isaacsim.core.version import get_version
from isaacsim.core.utils.extensions import enable_extension

EXTENSIONS = [
    "isaacsim.ros2.bridge",
    "omni.graph.window.action",
    "omni.kit.window.script_editor",
    "isaacsim.code_editor.vscode",
    "isaacsim.code_editor.jupyter",
]

print("Isaac Sim version: ", get_version())

for e in EXTENSIONS:
    enable_extension(e)
    simulation_app.update()

while simulation_app.is_running():
    simulation_app.update()

# Close the running Toolkit
simulation_app.close()
