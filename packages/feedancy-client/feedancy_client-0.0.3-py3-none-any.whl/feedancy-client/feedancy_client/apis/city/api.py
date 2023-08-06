from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import city_retrieve
from . import city_create
from . import city_retrieve_2
from . import city_update
from . import city_destroy
class CityApi(BaseApi):
    city_retrieve = city_retrieve.make_request
    city_create = city_create.make_request
    city_retrieve_2 = city_retrieve_2.make_request
    city_update = city_update.make_request
    city_destroy = city_destroy.make_request