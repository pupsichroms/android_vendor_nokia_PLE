#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
vendor_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
export PYTHONDONTWRITEBYTECODE=1
exec python3 "$vendor_dir/tools/prepare-vendor.py" "$@"
