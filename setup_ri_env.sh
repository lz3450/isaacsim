if [ -n "$BASH_VERSION" ]; then
    export SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    ROS2_SHELL="bash"
elif [ -n "$ZSH_VERSION" ]; then
    export SCRIPT_DIR="$(cd "$(dirname "${(%):-%x}")" && pwd)"
    ROS2_SHELL="zsh"
else
    echo "Unsupported shell"
    return 1
fi
echo "SCRIPT_DIR=$SCRIPT_DIR"

################################################################################

### Environment Variables
export PATH="$SCRIPT_DIR:$PATH"

### Domain ID
export ROS_DOMAIN_ID=77
echo "ROS_DOMAIN_ID=$ROS_DOMAIN_ID"

### RMW Implementation
export RMW_IMPLEMENTATION="rmw_fastrtps_cpp"
# export RMW_IMPLEMENTATION="rmw_cyclonedds_cpp"
echo "RMW_IMPLEMENTATION=$RMW_IMPLEMENTATION"

ROS2_JAZZY_SETUP="$SCRIPT_DIR/../ros2_ws/install/local_setup.$ROS2_SHELL"
# ROS2_JAZZY_SETUP="/opt/ros/jazzy/local_setup.$ROS2_SHELL"
if [ -f "$ROS2_JAZZY_SETUP" ]; then
    echo "ros2 ($ROS2_SHELL)"
    . "$ROS2_JAZZY_SETUP"
else
    echo "Failed to set up ros2_jazzy"
    return 1
fi

ISAAC_SIM_JAZZY_WS_SETUP="$SCRIPT_DIR/../IsaacSim-ros_workspaces/jazzy_ws/install/local_setup.$ROS2_SHELL"
if [ -f "$ISAAC_SIM_JAZZY_WS_SETUP" ]; then
    echo "isaac_sim_ros_ws ($ROS2_SHELL)"
    . "$ISAAC_SIM_JAZZY_WS_SETUP"
else
    echo "Failed to set up isaac_sim_jazzy_ws"
    return 1
fi
