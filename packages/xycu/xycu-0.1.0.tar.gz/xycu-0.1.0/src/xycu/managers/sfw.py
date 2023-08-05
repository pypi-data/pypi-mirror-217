"""sfw.py"""

import attrs
import requests

from ..models import images
from ..models.enums.categories import sfw


@attrs.define
class SfwManager:
    """SfwManager"""

    session: requests.Session

    def get(self, sfw_category: sfw.SfwCategory) -> images.Image:
        """get"""
        url = f"https://waifu.pics/api/sfw/{sfw_category.value}"
        response = self.session.get(url)

        image = images.Image(**response.json())

        return image
