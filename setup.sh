if [ -n "$BASH_VERSION" ]; then
  export ISAAC_SIM_ROOT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1; pwd -P)"
  shell="bash"
elif [ -n "$ZSH_VERSION" ]; then
  export ISAAC_SIM_ROOT_DIR="$(cd -- "$(dirname "${(%):-%x}")" > /dev/null 2>&1; pwd -P)"
  shell="zsh"
else
  echo "Unsupported shell"
  return
fi
echo "ISAAC_SIM_ROOT_DIR=$ISAAC_SIM_ROOT_DIR"

# export RMW_IMPLEMENTATION="rmw_fastrtps_cpp"
# export RMW_IMPLEMENTATION="rmw_cyclonedds_cpp"

ISAAC_SIM_ROS2_HUMBLE_SETUP="$ISAAC_SIM_ROOT_DIR/../IsaacSim-ros_workspaces/build_ws/humble/humble_ws/install/local_setup.$shell"
if [[ -f "$ISAAC_SIM_ROS2_HUMBLE_SETUP" ]]; then
    echo "isaac_sim_ros2_humble ($shell)"
    . "$ISAAC_SIM_ROS2_HUMBLE_SETUP"
fi

ISAAC_SIM_ROS2_WS_SETUP="$ISAAC_SIM_ROOT_DIR/../IsaacSim-ros_workspaces/build_ws/humble/isaac_sim_ros_ws/install/local_setup.$shell"
if [[ -f "$ISAAC_SIM_ROS2_WS_SETUP" ]]; then
    echo "isaac_sim_ros2_ws ($shell)"
    . "$ISAAC_SIM_ROS2_WS_SETUP"
fi

export PATH="$ISAAC_SIM_ROOT_DIR:$PATH"
export WAYLAND_DISPLAY="wayland-0"
export DISPLAY=":0"
