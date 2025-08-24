#!/usr/bin/env python.sh
#
# add_frankas.py
#


from isaacsim.simulation_app import SimulationApp

simulation_app = SimulationApp({"headless": False})

import sys

import carb
import numpy as np
from isaacsim.core.api import World
from isaacsim.core.api.robots import Robot
from isaacsim.core.utils.stage import add_reference_to_stage, get_stage_units
from isaacsim.core.utils.types import ArticulationAction
from isaacsim.storage.native import get_assets_root_path

assets_root_path = get_assets_root_path()
if assets_root_path is None:
    carb.log_error("Could not find Isaac Sim assets folder")
    simulation_app.close()
    sys.exit()

my_world = World(stage_units_in_meters=1.0)
my_world.scene.add_default_ground_plane()

asset_path = assets_root_path + "/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd"
robot1 = add_reference_to_stage(usd_path=asset_path, prim_path="/World/Franka_1")
robot1.GetVariantSet("Gripper").SetVariantSelection("AlternateFinger")
robot1.GetVariantSet("Mesh").SetVariantSelection("Quality")
robot2 = add_reference_to_stage(usd_path=asset_path, prim_path="/World/Franka_2")
robot2.GetVariantSet("Gripper").SetVariantSelection("AlternateFinger")
robot2.GetVariantSet("Mesh").SetVariantSelection("Quality")

articulated_system_1_name = "my_franka_1"
articulated_system_1 = Robot(prim_path="/World/Franka_1", name=articulated_system_1_name)
articulated_system_2_name = "my_franka_2"
articulated_system_2 = Robot(prim_path="/World/Franka_2", name=articulated_system_2_name)
my_world.scene.scene_registry.add_robot(articulated_system_1_name, articulated_system_1)
my_world.scene.scene_registry.add_robot(articulated_system_2_name, articulated_system_2)

for i in range(5):
    print("resetting...")
    my_world.reset()
    articulated_system_1.set_world_pose(position=(np.array([0.0, 2.0, 0.0]) / get_stage_units()).tolist())
    articulated_system_2.set_world_pose(position=(np.array([0.0, -2.0, 0.0]) / get_stage_units()).tolist())
    articulated_system_1.set_joint_positions(np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]))
    for j in range(500):
        my_world.step(render=True)
        if j == 100:
            articulated_system_2.get_articulation_controller().apply_action(
                ArticulationAction(joint_positions=np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]))
            )
        if j == 400:
            print("Franka 1's joint positions are: ", articulated_system_1.get_joint_positions())
            print("Franka 2's joint positions are: ", articulated_system_2.get_joint_positions())
simulation_app.close()
