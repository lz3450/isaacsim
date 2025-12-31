#!/bin/bash
#
# launch_task0.sh
#

set -e

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1; pwd -P)"

################################################################################

. "$SCRIPT_DIR"/../setup.sh

mkdir -p "$SCRIPT_DIR"/log
./tasks/task0.py > "$SCRIPT_DIR"/log/task0.log 2>&1 &

sleep 12

ros2 launch myisaacsim task0.launch.py
