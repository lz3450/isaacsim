#!/usr/bin/env python.sh
#
# task0.py
#

###
from isaacsim.simulation_app import SimulationApp

###
# https://docs.omniverse.nvidia.com/py/isaacsim/source/extensions/omni.isaac.kit/docs/index.html
simulation_app = SimulationApp({"headless": False})

###
import sys
import numpy as np

###
import carb
import omni.kit.commands
import omni.graph.core as og
from pxr import Gf
import usdrt.Sdf
from isaacsim.core.version import get_version
from isaacsim.core.utils.extensions import enable_extension
from isaacsim.storage.native import get_assets_root_path
from isaacsim.core.utils.viewports import set_camera_view
from isaacsim.core.utils.stage import add_reference_to_stage
from isaacsim.core.prims import XFormPrim
from isaacsim.core.utils.rotations import gf_rotation_to_np_array

###
EXTENSIONS = [
    "isaacsim.code_editor.jupyter",
    "isaacsim.code_editor.vscode",
    "isaacsim.ros2.bridge",
    "omni.graph.window.action",
    "omni.kit.window.script_editor",
]
FRANKA_STAGE_PATH = "/Franka"


###
print("Isaac Sim version: ", get_version())

###
for extension in EXTENSIONS:
    enable_extension(extension)

###
assets_root_path = get_assets_root_path()
if assets_root_path is None:
    carb.log_error("Failed to get assets root path")
    simulation_app.close()
    sys.exit(1)
print("Assets root path: ", assets_root_path)

set_camera_view(eye=[1.20, 1.20, 0.80], target=[0, 0, 0.50], camera_prim_path="/OmniverseKit_Persp")

franka = add_reference_to_stage(
    usd_path=assets_root_path + "/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd",
    prim_path=FRANKA_STAGE_PATH,
)
franka_xform = XFormPrim(
    prim_paths_expr=franka.GetName(),
    positions=np.array([0, -0.64, 0]).reshape(1, 3),
    orientations=gf_rotation_to_np_array(Gf.Rotation(Gf.Vec3d(0, 0, 1), 90)).reshape(1, 4),
)
background = add_reference_to_stage(
    usd_path=assets_root_path + "/Isaac/Environments/Simple_Room/simple_room.usd",
    prim_path="/background",
)
cracker_box = add_reference_to_stage(
    prim_path="/cracker_box",
    usd_path=assets_root_path + "/Isaac/Props/YCB/Axis_Aligned_Physics/003_cracker_box.usd",
)
cracker_box_xform = XFormPrim(
    prim_paths_expr=cracker_box.GetName(),
    positions=np.array([-0.2, -0.25, 0.1]).reshape(1, 3),
    orientations=gf_rotation_to_np_array(Gf.Rotation(Gf.Vec3d(1, 0, 0), -90)).reshape(1, 4),
)

###
og.Controller.edit(
    {"graph_path": "/ActionGraph", "evaluator_name": "execution"},
    {
        og.Controller.Keys.CREATE_NODES: [
            ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
            ("ReadSimTime", "isaacsim.core.nodes.IsaacReadSimulationTime"),
            ("Context", "isaacsim.ros2.bridge.ROS2Context"),
            ("PublishJointState", "isaacsim.ros2.bridge.ROS2PublishJointState"),
            ("SubscribeJointState", "isaacsim.ros2.bridge.ROS2SubscribeJointState"),
            ("ArticulationController", "isaacsim.core.nodes.IsaacArticulationController"),
            ("PublishClock", "isaacsim.ros2.bridge.ROS2PublishClock"),
        ],
        og.Controller.Keys.CONNECT: [
            ("OnPlaybackTick.outputs:tick", "PublishJointState.inputs:execIn"),
            ("OnPlaybackTick.outputs:tick", "SubscribeJointState.inputs:execIn"),
            ("OnPlaybackTick.outputs:tick", "PublishClock.inputs:execIn"),
            ("OnPlaybackTick.outputs:tick", "ArticulationController.inputs:execIn"),
            ("Context.outputs:context", "PublishJointState.inputs:context"),
            ("Context.outputs:context", "SubscribeJointState.inputs:context"),
            ("Context.outputs:context", "PublishClock.inputs:context"),
            ("ReadSimTime.outputs:simulationTime", "PublishJointState.inputs:timeStamp"),
            ("ReadSimTime.outputs:simulationTime", "PublishClock.inputs:timeStamp"),
            ("SubscribeJointState.outputs:jointNames", "ArticulationController.inputs:jointNames"),
            ("SubscribeJointState.outputs:positionCommand", "ArticulationController.inputs:positionCommand"),
            ("SubscribeJointState.outputs:velocityCommand", "ArticulationController.inputs:velocityCommand"),
            ("SubscribeJointState.outputs:effortCommand", "ArticulationController.inputs:effortCommand"),
        ],
        og.Controller.Keys.SET_VALUES: [
            ("ArticulationController.inputs:robotPath", FRANKA_STAGE_PATH),
            ("PublishJointState.inputs:topicName", "isaac_joint_states"),
            ("SubscribeJointState.inputs:topicName", "isaac_joint_commands"),
            ("PublishJointState.inputs:targetPrim", [usdrt.Sdf.Path(FRANKA_STAGE_PATH)]),
        ],
    },
)

###
while simulation_app.is_running():
    simulation_app.update()

###
simulation_app.close()
