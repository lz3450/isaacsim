if [ -n "$BASH_VERSION" ]; then
  export ISAAC_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1; pwd -P)"
elif [ -n "$ZSH_VERSION" ]; then
  export ISAAC_DIR="$(cd -- "$(dirname "${(%):-%x}")" > /dev/null 2>&1; pwd -P)"
else
  echo "Unsupported shell"
fi

. ../RoboTrace/moveit2_ws/moveit2_setup.sh
echo "ISAAC_DIR=$ISAAC_DIR"
export PATH="$ISAAC_DIR:$ISAAC_DIR/kit/python/bin:$PATH"
