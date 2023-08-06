# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

"""
Import this module to initialize the libdnf5_cli shim
"""

from __future__ import annotations

from ._impl import initialize

initialize("libdnf5_cli")
