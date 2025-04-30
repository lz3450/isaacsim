import os
from typing import List, Tuple, Any
import carb

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

FRANKA_STAGE_PATH = "/Franka"
FRANKA_USD_PATH = "/Isaac/Robots/Franka/franka_alt_fingers.usd"

BACKGROUND_STAGE_PATH = "/background"
BACKGROUND_USD_PATH = "/Isaac/Environments/Simple_Room/simple_room.usd"

GRAPH_PATH = "/ActionGraph"


def get_ros_domain_id() -> int:
    try:
        return int(os.environ.get("ROS_DOMAIN_ID", 0))
    except ValueError:
        return 0


def get_action_graph_nodes() -> List[Tuple[str, Any]]:
    return [
        ("ArticulationController", "isaacsim.core.nodes.IsaacArticulationController"),
        ("Context", "isaacsim.ros2.bridge.ROS2Context"),
        ("OnImpulseEvent", "omni.graph.action.OnImpulseEvent"),
        ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
        ("PublishClock", "isaacsim.ros2.bridge.ROS2PublishClock"),
        ("PublishJointState", "isaacsim.ros2.bridge.ROS2PublishJointState"),
        ("ReadSimTime", "isaacsim.core.nodes.IsaacReadSimulationTime"),
        ("SubscribeJointState", "isaacsim.ros2.bridge.ROS2SubscribeJointState"),
    ]


def get_action_graph_connections() -> List[Tuple[str, Any]]:
    return [
        ("Context.outputs:context", "PublishClock.inputs:context"),
        ("OnImpulseEvent.outputs:execOut", "PublishClock.inputs:execIn"),
        ("OnPlaybackTick.outputs:tick", "ArticulationController.inputs:execIn"),
        ("OnPlaybackTick.outputs:tick", "PublishJointState.inputs:execIn"),
        ("OnPlaybackTick.outputs:tick", "SubscribeJointState.inputs:execIn"),
        ("ReadSimTime.outputs:simulationTime", "PublishClock.inputs:timeStamp"),
        ("ReadSimTime.outputs:simulationTime", "PublishJointState.inputs:timeStamp"),
        ("SubscribeJointState.outputs:effortCommand", "ArticulationController.inputs:effortCommand"),
        ("SubscribeJointState.outputs:jointNames", "ArticulationController.inputs:jointNames"),
        ("SubscribeJointState.outputs:positionCommand", "ArticulationController.inputs:positionCommand"),
        ("SubscribeJointState.outputs:velocityCommand", "ArticulationController.inputs:velocityCommand"),
    ]


def get_action_graph_values(ros_domain_id: int) -> List[Tuple[str, Any]]:
    return [
        ("Context.inputs:domain_id", ros_domain_id),
        ("ArticulationController.inputs:robotPath", FRANKA_STAGE_PATH),
        ("PublishJointState.inputs:topicName", "joint_states"),
        ("SubscribeJointState.inputs:topicName", "joint_commands"),
    ]


def main() -> int:
    carb.log_info(f"Isaac Sim version: {get_version()}")

    # Enable ROS2 bridge extension
    enable_extension("isaacsim.ros2.bridge")
    # Enable ROS2 and action graph UI
    enable_extension("omni.graph.window.action")

    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        carb.log_error("Could not find Isaac Sim assets folder")
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
            og.Controller.Keys.CONNECT: get_action_graph_connections(),
            og.Controller.Keys.SET_VALUES: get_action_graph_values(get_ros_domain_id()),
        },
    )

    set_targets(
        prim=get_current_stage().GetPrimAtPath("/ActionGraph/PublishJointState"),
        attribute="inputs:targetPrim",
        target_prim_paths=[FRANKA_STAGE_PATH],
    )

    return 0


if __name__ == "__main__":
    main()
