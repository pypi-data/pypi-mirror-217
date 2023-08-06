"""🍂 An unofficial Waifu.pics API wrapper for Python"""

# ruff: noqa: F401

from .clients import Client
from .managers.nsfw import NsfwManager
from .managers.sfw import SfwManager
from .models.enums.categories.nsfw import NsfwCategory
from .models.enums.categories.sfw import SfwCategory
from .models.images import Image
