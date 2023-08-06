from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import companycity_retrieve
from . import companycity_create
from . import companycity_retrieve_2
from . import companycity_update
from . import companycity_destroy
class CompanycityApi(BaseApi):
    companycity_retrieve = companycity_retrieve.make_request
    companycity_create = companycity_create.make_request
    companycity_retrieve_2 = companycity_retrieve_2.make_request
    companycity_update = companycity_update.make_request
    companycity_destroy = companycity_destroy.make_request