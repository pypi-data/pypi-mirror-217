# =====================================
# generator=datazen
# version=3.1.2
# hash=325e245e0e7b4e7366d426ca615de809
# =====================================

"""
A module aggregating package commands.
"""

# built-in
from typing import List as _List
from typing import Tuple as _Tuple

# third-party
from vcorelib.args import CommandRegister as _CommandRegister

# internal
from yambs.commands.gen import add_gen_cmd
from yambs.commands.native import add_native_cmd
from yambs.commands.uf2conv import add_uf2conv_cmd


def commands() -> _List[_Tuple[str, str, _CommandRegister]]:
    """Get this package's commands."""

    return [
        (
            "gen",
            "poll the source tree and generate any new build files",
            add_gen_cmd,
        ),
        (
            "native",
            "generate build files for native-only target projects",
            add_native_cmd,
        ),
        (
            "uf2conv",
            "Convert to UF2 or flash directly.",
            add_uf2conv_cmd,
        ),
        ("noop", "command stub (does nothing)", lambda _: lambda _: 0),
    ]
