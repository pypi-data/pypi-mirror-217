from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import contact_retrieve
from . import contact_create
from . import contact_retrieve_2
from . import contact_update
from . import contact_destroy
class ContactApi(BaseApi):
    contact_retrieve = contact_retrieve.make_request
    contact_create = contact_create.make_request
    contact_retrieve_2 = contact_retrieve_2.make_request
    contact_update = contact_update.make_request
    contact_destroy = contact_destroy.make_request