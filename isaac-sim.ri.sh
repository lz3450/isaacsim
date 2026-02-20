#!/usr/bin/env bash

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export RESOURCE_NAME="IsaacSim"
export OLD_PYTHONPATH=$PYTHONPATH

### Domain ID
export ROS_DOMAIN_ID=77
echo "ROS_DOMAIN_ID=$ROS_DOMAIN_ID"

### RMW Implementation
export RMW_IMPLEMENTATION="rmw_fastrtps_cpp"
# export RMW_IMPLEMENTATION="rmw_cyclonedds_cpp"
echo "RMW_IMPLEMENTATION=$RMW_IMPLEMENTATION"

ISAAC_SIM_ROS_JAZZY_SETUP="$SCRIPT_DIR/../IsaacSim-ros_workspaces/build_ws/jazzy/jazzy_ws/install/local_setup.bash"
if [ -f "$ISAAC_SIM_ROS_JAZZY_SETUP" ]; then
    echo "isaac_sim_ros_jazzy"
    . "$ISAAC_SIM_ROS_JAZZY_SETUP"
fi

ISAAC_SIM_ROS_WS_SETUP="$SCRIPT_DIR/../IsaacSim-ros_workspaces/build_ws/jazzy/isaac_sim_ros_ws/install/local_setup.bash"
if [ -f "$ISAAC_SIM_ROS_WS_SETUP" ]; then
    echo "isaac_sim_ros_ws"
    . "$ISAAC_SIM_ROS_WS_SETUP"
fi

exec "$SCRIPT_DIR/kit/kit" "$SCRIPT_DIR/apps/isaacsim.exp.selector.kit" "$@"
