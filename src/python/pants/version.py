# Copyright 2017 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import os

from packaging.version import Version

# Generate a inferrable dependency on the `pants._version` package and its associated resources.
import pants._version
from pants.util.resources import read_resource

# Set this env var to override the version pants reports. Useful for testing.
_PANTS_VERSION_OVERRIDE = "_PANTS_VERSION_OVERRIDE"


VERSION: str = (
    os.environ.get(_PANTS_VERSION_OVERRIDE)
    or
    # NB: We expect VERSION to always have an entry and want a runtime failure if this is false.
    # `pants._version` is a non-namespace package that can be loaded by `importlib.resources` in
    # pre-3.11 versions of Python. Once we can read `pants.VERSION` using the resource loader,
    # we can remove the `pants._version` package. See #16379.
    read_resource(pants._version.__name__, "VERSION").decode().strip()
)

PANTS_SEMVER = Version(VERSION)

# E.g. 2.0 or 2.2.
MAJOR_MINOR = f"{PANTS_SEMVER.major}.{PANTS_SEMVER.minor}"
