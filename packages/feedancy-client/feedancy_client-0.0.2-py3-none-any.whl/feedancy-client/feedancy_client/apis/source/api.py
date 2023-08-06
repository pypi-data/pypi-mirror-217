from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import source_retrieve
from . import source_create
from . import source_retrieve_2
from . import source_update
from . import source_destroy
class SourceApi(BaseApi):
    source_retrieve = source_retrieve.make_request
    source_create = source_create.make_request
    source_retrieve_2 = source_retrieve_2.make_request
    source_update = source_update.make_request
    source_destroy = source_destroy.make_request