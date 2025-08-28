#!/usr/bin/env python.sh
#
# test3.py
#
# Test for World
#

###
from isaacsim.simulation_app import SimulationApp

# https://docs.omniverse.nvidia.com/py/isaacsim/source/extensions/omni.isaac.kit/docs/index.html
simulation_app = SimulationApp({"headless": False})

###
from isaacsim.core.api import World
from isaacsim.core.utils.extensions import enable_extension

###
EXTENSIONS = [
    "isaacsim.code_editor.jupyter",
    "isaacsim.code_editor.vscode",
    "isaacsim.ros2.bridge",
    "omni.graph.window.action",
    "omni.kit.window.script_editor",
]

for e in EXTENSIONS:
    enable_extension(e)
    simulation_app.update()

world = World(stage_units_in_meters=1.0)

world.add_default_ground_plane()

world.reset()

while simulation_app.is_running():
    world.step(render=True)

# Close the running Toolkit
simulation_app.close()
