import attrs
import requests

from .managers import nsfw, sfw


@attrs.define
class Client:
    _session = requests.Session()

    _nsfw_manager = nsfw.NsfwManager(_session)
    _sfw_manager = sfw.SfwManager(_session)

    @property
    def nsfw(self) -> nsfw.NsfwManager:
        return self._nsfw_manager

    @property
    def sfw(self) -> sfw.SfwManager:
        return self._sfw_manager
