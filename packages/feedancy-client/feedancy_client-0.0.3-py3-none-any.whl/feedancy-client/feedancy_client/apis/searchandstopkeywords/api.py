from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import searchandstopkeywords_retrieve
from . import searchandstopkeywords_create
from . import searchandstopkeywords_retrieve_2
from . import searchandstopkeywords_update
from . import searchandstopkeywords_destroy
class SearchandstopkeywordsApi(BaseApi):
    searchandstopkeywords_retrieve = searchandstopkeywords_retrieve.make_request
    searchandstopkeywords_create = searchandstopkeywords_create.make_request
    searchandstopkeywords_retrieve_2 = searchandstopkeywords_retrieve_2.make_request
    searchandstopkeywords_update = searchandstopkeywords_update.make_request
    searchandstopkeywords_destroy = searchandstopkeywords_destroy.make_request