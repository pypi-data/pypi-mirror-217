<!--
Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
SPDX-License-Identifier: MIT
-->

NEWS
======

## 0.1.0 - 2023-07-02 <a id='0.1.0'></a>

### Added

- Add shim module for `libdnf5_cli`
- pyproject.toml: add `Homepage` to `[project.urls]`

### Changed

- Make `libdnf5` a single-file module instead of a package.
  In case of installation conflicts, `libdnf5/__init__.py` has priority over
  `libdnf5.py`.

## 0.0.1 - 2023-06-19 <a id='0.0.1'></a>

Initial release

