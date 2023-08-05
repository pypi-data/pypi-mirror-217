"""nsfw.py"""

import attrs
import requests

from ..models import images
from ..models.enums.categories import nsfw


@attrs.define
class NsfwManager:
    """NsfwManager"""

    session: requests.Session

    def get(self, nsfw_category: nsfw.NsfwCategory) -> images.Image:
        """get"""
        url = f"https://waifu.pics/api/nsfw/{nsfw_category.value}"
        response = self.session.get(url)

        image = images.Image(**response.json())

        return image
