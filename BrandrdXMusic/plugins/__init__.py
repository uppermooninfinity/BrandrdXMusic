import glob
import os
from os.path import dirname, isfile

# List of modules that should load first (primary/error-prone)
PRIMARY_MODULES = [
    "admin.skip",        # example: your play command
    "play.play",        # example: call handling
    "admin.seek"  # example: any critical music handler
]

def __list_all_modules():
    work_dir = dirname(__file__)
    mod_paths = glob.glob(os.path.join(work_dir, "*", "*.py"))

    all_modules = [
        (((f.replace(work_dir, "")).replace("/", "."))[:-3])
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    # Separate primary modules from the rest
    primary = [m for m in PRIMARY_MODULES if m in all_modules]
    remaining = [m for m in all_modules if m not in PRIMARY_MODULES]

    # Return primary first, then remaining sorted
    return primary + sorted(remaining)

ALL_MODULES = __list_all_modules()
__all__ = ALL_MODULES + ["ALL_MODULES"]
