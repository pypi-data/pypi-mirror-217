from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import jobmixin_retrieve
from . import jobmixin_create
from . import jobmixin_retrieve_2
from . import jobmixin_update
from . import jobmixin_destroy
class JobmixinApi(BaseApi):
    jobmixin_retrieve = jobmixin_retrieve.make_request
    jobmixin_create = jobmixin_create.make_request
    jobmixin_retrieve_2 = jobmixin_retrieve_2.make_request
    jobmixin_update = jobmixin_update.make_request
    jobmixin_destroy = jobmixin_destroy.make_request