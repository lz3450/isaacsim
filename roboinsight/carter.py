#!/usr/bin/env python.sh
#
# carter.py
#

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--headless", type=bool, default=False)
args = parser.parse_args()

from isaacsim.simulation_app import SimulationApp

simulation_app = SimulationApp({"headless": args.headless})

from isaacsim.core.utils.extensions import enable_extension
from isaacsim.storage.native import get_assets_root_path
from isaacsim.core.utils.stage import open_stage
from isaacsim.core.api import World

EXTENSIONS = [
    "isaacsim.ros2.bridge",
    "omni.graph.window.action",
    "omni.kit.window.script_editor",
    "isaacsim.code_editor.vscode",
    "isaacsim.code_editor.jupyter",
]

for e in EXTENSIONS:
    enable_extension(e)
    simulation_app.update()

assets_root = get_assets_root_path()
if assets_root is None:
    raise RuntimeError("Could not find Isaac Sim assets root")

stage_path = assets_root + "/Isaac/Samples/ROS2/Scenario/carter_warehouse_navigation.usd"

print("Loading stage:", stage_path)

open_stage(stage_path)

world = World()
world.reset()

while simulation_app.is_running():
    world.step(render=True)

simulation_app.close()
