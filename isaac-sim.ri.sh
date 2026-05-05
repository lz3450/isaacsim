#!/usr/bin/env bash

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export RESOURCE_NAME="IsaacSim"
export OLD_PYTHONPATH=$PYTHONPATH

. "$SCRIPT_DIR/setup_ri_env.sh"

exec "$SCRIPT_DIR/kit/kit" "$SCRIPT_DIR/apps/isaacsim.exp.selector.kit" "$@"
