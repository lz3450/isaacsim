#!/usr/bin/env bash

set -e

export RESOURCE_NAME="IsaacSim"
export OLD_PYTHONPATH=$PYTHONPATH

unset SCRIPT_DIR
. ./setup_ri_env.sh

exec "$SCRIPT_DIR/kit/kit" "$SCRIPT_DIR/apps/isaacsim.exp.full.kit" "$@"
