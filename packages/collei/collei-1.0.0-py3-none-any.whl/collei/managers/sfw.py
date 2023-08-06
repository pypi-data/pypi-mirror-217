import attrs
import requests

from ..models import images
from ..models.enums.categories import sfw


@attrs.define
class SfwManager:
    session: requests.Session

    def get(self, sfw_category: sfw.SfwCategory) -> images.Image:
        url = f"https://api.waifu.pics/sfw/{sfw_category.value}"
        response = self.session.get(url)

        image = images.Image(**response.json())

        return image
