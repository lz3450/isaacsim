#!/home/kzl/Projects/isaacsim/python.sh

import sys
import os
from typing import List, Tuple, Any
import numpy as np
import carb

CONFIG = {
    "renderer": "RayTracedLighting",
    "headless": False,
}

FRANKA_STAGE_PATH = "/Franka"
FRANKA_USD_PATH = "/Isaac/Robots/Franka/franka_alt_fingers.usd"

BACKGROUND_STAGE_PATH = "/background"
BACKGROUND_USD_PATH = "/Isaac/Environments/Simple_Room/simple_room.usd"

GRAPH_PATH = "/ActionGraph"


def get_ros_domain_id() -> int:
    try:
        ros_domain_id = int(os.environ["ROS_DOMAIN_ID"])
        carb.log_info(f"Using ROS_DOMAIN_ID: {ros_domain_id}")
    except ValueError:
        carb.log_warn("Invalid ROS_DOMAIN_ID integer value. Setting value to 0")
        ros_domain_id = 0
    except KeyError:
        carb.log_info("ROS_DOMAIN_ID environment variable is not set. Setting value to 0")
        ros_domain_id = 0

    return ros_domain_id


def get_action_graph_nodes() -> List[Tuple[str, Any]]:
    return [
        ("OnImpulseEvent", "omni.graph.action.OnImpulseEvent"),
        ("ReadSimTime", "isaacsim.core.nodes.IsaacReadSimulationTime"),
        ("Context", "isaacsim.ros2.bridge.ROS2Context"),
        ("PublishJointState", "isaacsim.ros2.bridge.ROS2PublishJointState"),
        ("PublishClock", "isaacsim.ros2.bridge.ROS2PublishClock"),
        ("OnTick", "omni.graph.action.OnTick"),
    ]


def get_action_graph_connect() -> List[Tuple[str, Any]]:
    return [
        ("OnImpulseEvent.outputs:execOut", "PublishJointState.inputs:execIn"),
        ("Context.outputs:context", "PublishJointState.inputs:context"),
        ("Context.outputs:context", "PublishClock.inputs:context"),
        ("ReadSimTime.outputs:simulationTime", "PublishJointState.inputs:timeStamp"),
        ("ReadSimTime.outputs:simulationTime", "PublishClock.inputs:timeStamp"),
    ]


def get_action_graph_values(ros_domain_id: int) -> List[Tuple[str, Any]]:
    return [
        ("Context.inputs:domain_id", ros_domain_id),
        ("PublishJointState.inputs:topicName", "isaac_joint_states"),
    ]


def main() -> int:
    from isaacsim.simulation_app import SimulationApp

    simulation_app = SimulationApp(CONFIG)

    from isaacsim.core.version import get_version
    from isaacsim.core.api import World
    from isaacsim.core.utils.extensions import enable_extension
    from isaacsim.core.utils.stage import add_reference_to_stage, get_current_stage
    from isaacsim.core.utils.nucleus import get_assets_root_path
    from isaacsim.core.utils.viewports import set_camera_view
    from isaacsim.core.utils.rotations import gf_rotation_to_np_array
    from isaacsim.core.utils.prims import create_prim, set_targets
    from pxr import Gf
    import omni.graph.core as og

    carb.log_info(f"Isaac Sim version: {get_version()}")

    # Enable ROS2 bridge extension
    enable_extension("isaacsim.ros2.bridge")
    # Enable ROS2 and action graph UI
    enable_extension("omni.graph.window.action")

    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        carb.log_error("Could not find Isaac Sim assets folder")
        simulation_app.close()
        return -1

    world = World(stage_units_in_meters=1.0)
    # Prepare stage
    set_camera_view(eye=[1.2, 1.2, 0.8], target=[0, 0, 0.5])
    # Load environment and robot
    add_reference_to_stage(assets_root_path + BACKGROUND_USD_PATH, BACKGROUND_STAGE_PATH)

    create_prim(
        FRANKA_STAGE_PATH,
        "Xform",
        position=[0, -0.64, 0],
        orientation=gf_rotation_to_np_array(Gf.Rotation(Gf.Vec3d(0, 0, 1), 90)).tolist(),
        usd_path=assets_root_path + FRANKA_USD_PATH,
    )
    create_prim(
        "/cracker_box",
        "Xform",
        position=[-0.2, -0.25, 0.1],
        orientation=gf_rotation_to_np_array(Gf.Rotation(Gf.Vec3d(1, 0, 0), -90)).tolist(),
        usd_path=assets_root_path + "/Isaac/Props/YCB/Axis_Aligned_Physics/003_cracker_box.usd",
    )
    create_prim(
        "/sugar_box",
        "Xform",
        position=[-0.1, -0.25, 0.1],
        orientation=gf_rotation_to_np_array(Gf.Rotation(Gf.Vec3d(0, 1, 0), -90)).tolist(),
        usd_path=assets_root_path + "/Isaac/Props/YCB/Axis_Aligned_Physics/004_sugar_box.usd",
    )

    og.Controller.edit(
        {"graph_path": GRAPH_PATH, "evaluator_name": "execution"},
        {
            og.Controller.Keys.CREATE_NODES: get_action_graph_nodes(),
            og.Controller.Keys.CONNECT: get_action_graph_connect(),
            og.Controller.Keys.SET_VALUES: get_action_graph_values(get_ros_domain_id()),
        },
    )

    set_targets(
        prim=get_current_stage().GetPrimAtPath("/ActionGraph/PublishJointState"),
        attribute="inputs:targetPrim",
        target_prim_paths=[FRANKA_STAGE_PATH],
    )

    world.reset()
    simulation_app.update()

    while simulation_app.is_running():
        world.step(render=True)

        # Tick the Publish/Subscribe JointState, Publish TF and Publish Clock nodes each frame
        og.Controller.set(og.Controller.attribute("/ActionGraph/OnImpulseEvent.state:enableImpulse"), True)

    simulation_app.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
