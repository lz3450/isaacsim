#!/usr/bin/env python.sh
#
# task2.py
#
# Test for stage creation
#

# Import and launch the Omniverse Toolkit before any other imports.
# Note: Omniverse loads various plugins at runtime which
# cannot be imported unless the Toolkit is already running.
from isaacsim.simulation_app import SimulationApp

import sys

# See DEFAULT_LAUNCHER_CONFIG for available configuration
# https://docs.omniverse.nvidia.com/py/isaacsim/source/extensions/omni.isaac.kit/docs/index.html
simulation_app = SimulationApp({"headless": False})

# Locate any other import statement after this point
from isaacsim.core.version import get_version
from isaacsim.core.utils.extensions import enable_extension
from isaacsim.core.utils.nucleus import get_assets_root_path
from isaacsim.core.utils.viewports import set_camera_view
from isaacsim.core.utils.stage import add_reference_to_stage
from isaacsim.core.utils.prims import create_prim
from isaacsim.core.utils.rotations import gf_rotation_to_np_array
from pxr import Gf
import carb

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

assets_root_path = get_assets_root_path()
if assets_root_path is None:
    carb.log_error("Could not find Isaac Sim assets folder")
    sys.exit(1)
print("Assets root path: ", assets_root_path)

set_camera_view(eye=[1.2, 1.2, 0.8], target=[0, 0, 0.5])
add_reference_to_stage(assets_root_path + "/Isaac/Environments/Simple_Room/simple_room.usd", "/background")

create_prim(
    prim_path="/Franka",
    position=[0, -0.64, 0],
    orientation=gf_rotation_to_np_array(Gf.Rotation(Gf.Vec3d(0, 0, 1), 90)).tolist(),
    usd_path=assets_root_path + "/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd",
)
create_prim(
    prim_path="/cracker_box",
    position=[-0.2, -0.25, 0.1],
    orientation=gf_rotation_to_np_array(Gf.Rotation(Gf.Vec3d(1, 0, 0), -90)).tolist(),
    usd_path=assets_root_path + "/Isaac/Props/YCB/Axis_Aligned_Physics/003_cracker_box.usd",
)
create_prim(
    prim_path="/sugar_box",
    position=[0.2, -0.25, 0.05],
    orientation=gf_rotation_to_np_array(Gf.Rotation(Gf.Vec3d(0, 1, 0), -90)).tolist(),
    usd_path=assets_root_path + "/Isaac/Props/YCB/Axis_Aligned_Physics/004_sugar_box.usd",
)

while simulation_app.is_running():
    simulation_app.update()

# Close the running Toolkit
simulation_app.close()
