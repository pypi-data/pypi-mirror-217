from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import stopkeywords_retrieve
from . import stopkeywords_create
from . import stopkeywords_retrieve_2
from . import stopkeywords_update
from . import stopkeywords_destroy
class StopkeywordsApi(BaseApi):
    stopkeywords_retrieve = stopkeywords_retrieve.make_request
    stopkeywords_create = stopkeywords_create.make_request
    stopkeywords_retrieve_2 = stopkeywords_retrieve_2.make_request
    stopkeywords_update = stopkeywords_update.make_request
    stopkeywords_destroy = stopkeywords_destroy.make_request