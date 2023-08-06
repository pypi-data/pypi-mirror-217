from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import country_retrieve
from . import country_create
from . import country_retrieve_2
from . import country_update
from . import country_destroy
class CountryApi(BaseApi):
    country_retrieve = country_retrieve.make_request
    country_create = country_create.make_request
    country_retrieve_2 = country_retrieve_2.make_request
    country_update = country_update.make_request
    country_destroy = country_destroy.make_request