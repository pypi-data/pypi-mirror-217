"""nsfw.py"""

import enum
import typing


@typing.final
class NsfwCategory(str, enum.Enum):
    """NsfwCategory"""

    WAIFU = "waifu"
    NEKO = "neko"
    TRAP = "trap"
    BLOWJOB = "blowjob"
