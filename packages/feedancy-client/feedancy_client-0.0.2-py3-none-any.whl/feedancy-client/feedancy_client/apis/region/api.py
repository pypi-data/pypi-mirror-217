from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import region_retrieve
from . import region_create
from . import region_retrieve_2
from . import region_update
from . import region_destroy
class RegionApi(BaseApi):
    region_retrieve = region_retrieve.make_request
    region_create = region_create.make_request
    region_retrieve_2 = region_retrieve_2.make_request
    region_update = region_update.make_request
    region_destroy = region_destroy.make_request