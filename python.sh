#!/bin/bash
# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1; pwd -P)"
PYTHONEXE="$SCRIPT_DIR/kit/python/bin/python3"

export CARB_APP_PATH="$SCRIPT_DIR/kit"
export ISAAC_PATH="$SCRIPT_DIR"
export EXP_PATH="$SCRIPT_DIR/apps"

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$SCRIPT_DIR:$SCRIPT_DIR/exts/isaacsim.robot.schema/plugins/lib:$SCRIPT_DIR/exts/isaacsim.robot_motion.lula/pip_prebundle:$SCRIPT_DIR/exts/isaacsim.asset.exporter.urdf/pip_prebundle:$SCRIPT_DIR/kit:$SCRIPT_DIR/kit/kernel/plugins:$SCRIPT_DIR/kit/libs/iray:$SCRIPT_DIR/kit/plugins:$SCRIPT_DIR/kit/plugins/bindings-python:$SCRIPT_DIR/kit/plugins/carb_gfx:$SCRIPT_DIR/kit/plugins/rtx:$SCRIPT_DIR/kit/plugins/gpu.foundation"
export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR/kit/python/lib/python3.11:$SCRIPT_DIR/kit/python/lib/python3.11/site-packages:$SCRIPT_DIR/python_packages:$SCRIPT_DIR/exts/isaacsim.simulation_app:$SCRIPT_DIR/extsDeprecated/omni.isaac.kit:$SCRIPT_DIR/kit/kernel/py:$SCRIPT_DIR/kit/plugins/bindings-python:$SCRIPT_DIR/exts/isaacsim.robot_motion.lula/pip_prebundle:$SCRIPT_DIR/exts/isaacsim.asset.exporter.urdf/pip_prebundle:$SCRIPT_DIR/extscache/omni.kit.pip_archive-0.0.0+8131b85d.lx64.cp311/pip_prebundle:$SCRIPT_DIR/exts/omni.isaac.core_archive/pip_prebundle:$SCRIPT_DIR/exts/omni.isaac.ml_archive/pip_prebundle:$SCRIPT_DIR/exts/omni.pip.compute/pip_prebundle:$SCRIPT_DIR/exts/omni.pip.cloud/pip_prebundle"

export RESOURCE_NAME="IsaacSim"
export LD_PRELOAD="$SCRIPT_DIR/kit/libcarb.so"

PYTHONEXE="$SCRIPT_DIR/kit/python/bin/python3"

$PYTHONEXE "$@" || (echo "Failed to run $PYTHONEXE $@" && exit 127)
