if [ -n "$BASH_VERSION" ]; then
  export ISAAC_SIM_ROOT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1; pwd -P)"
elif [ -n "$ZSH_VERSION" ]; then
  export ISAAC_SIM_ROOT_DIR="$(cd -- "$(dirname "${(%):-%x}")" > /dev/null 2>&1; pwd -P)"
else
  echo "Unsupported shell"
fi

echo "ISAAC_SIM_ROOT_DIR=$ISAAC_SIM_ROOT_DIR"
export PATH="$ISAAC_SIM_ROOT_DIR:$PATH"
