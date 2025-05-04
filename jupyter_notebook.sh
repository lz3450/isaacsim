#!/bin/bash

set -e

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1; pwd -P)"
PYTHONEXE=${SCRIPT_DIR}/kit/python/bin/python3

export ISAAC_PATH="$SCRIPT_DIR"
export CARB_APP_PATH="$SCRIPT_DIR/kit"
export EXP_PATH="$SCRIPT_DIR/apps"

export PATH="$SCRIPT_DIR:$SCRIPT_DIR/kit/python/bin:$PATH"
export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR/kit/python/lib/python3.10:$SCRIPT_DIR/kit/python/lib/python3.10/site-packages:$SCRIPT_DIR/exts/isaacsim.simulation_app:$SCRIPT_DIR/extsDeprecated/omni.isaac.kit:$SCRIPT_DIR/kit/kernel/py:$SCRIPT_DIR/kit/plugins/bindings-python:$SCRIPT_DIR/exts/isaacsim.robot_motion.lula/pip_prebundle:$SCRIPT_DIR/exts/isaacsim.asset.exporter.urdf/pip_prebundle:$SCRIPT_DIR/extscache/omni.kit.pip_archive-0.0.0+d02c707b.lx64.cp310/pip_prebundle:$SCRIPT_DIR/exts/omni.isaac.core_archive/pip_prebundle:$SCRIPT_DIR/exts/omni.isaac.ml_archive/pip_prebundle:$SCRIPT_DIR/exts/omni.pip.compute/pip_prebundle:$SCRIPT_DIR/exts/omni.pip.cloud/pip_prebundle"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$SCRIPT_DIR/exts/omni.usd.schema.isaac/plugins/IsaacSensorSchema/lib:$SCRIPT_DIR/exts/omni.usd.schema.isaac/plugins/RangeSensorSchema/lib:$SCRIPT_DIR/exts/isaacsim.robot_motion.lula/pip_prebundle:$SCRIPT_DIR/exts/isaacsim.asset.exporter.urdf/pip_prebundle:$SCRIPT_DIR/kit:$SCRIPT_DIR/kit/kernel/plugins:$SCRIPT_DIR/kit/libs/iray:$SCRIPT_DIR/kit/plugins:$SCRIPT_DIR/kit/plugins/bindings-python:$SCRIPT_DIR/kit/plugins/carb_gfx:$SCRIPT_DIR/kit/plugins/rtx:$SCRIPT_DIR/kit/plugins/gpu.foundation"

"$PYTHONEXE" -m pip wheel --wheel-dir "$ISAAC_PATH/wheels" --no-binary :all: jupyter
"$PYTHONEXE" -m pip install --user -U --no-index --find-links "$ISAAC_PATH/wheels" jupyter

# Configure kernelspec based on current `python` path
KERNEL_DIR=$(mktemp -d)
cp -r "$SCRIPT_DIR"/jupyter_kernel "$KERNEL_DIR"
sed -i 's,AUTOMATICALLY_REPLACED,'"${PYTHONEXE}"',' "$KERNEL_DIR"/jupyter_kernel/kernel.json
# Add the kernelspec to jupyter notebook
jupyter kernelspec install "$KERNEL_DIR"/jupyter_kernel --name isaac_sim_python3 --user
# Remove temp dir for kernel once installed
rm -rf "$KERNEL_DIR"

# If the user provides the argument test as the first argument,
# we attempt to run the notebook in place via commandline and exit
if [[ $1 == "test" ]]; then
    shift
    jupyter nbconvert --ExecutePreprocessor.timeout=600 --ExecutePreprocessor.kernel_name="isaac_sim_python3" --to notebook --execute --output=/tmp/isaac_test.ipynb "$@" || (echo "Failed to run $PYTHONEXE $@" && exit 127)
else
    jupyter notebook --MappingKernelManager.default_kernel_name="Isaac Sim Python 3" "$@" || (echo "Failed to run $PYTHONEXE $@" && exit 127)
fi
