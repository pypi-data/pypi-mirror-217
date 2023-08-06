from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import searchkeywords_retrieve
from . import searchkeywords_create
from . import searchkeywords_retrieve_2
from . import searchkeywords_update
from . import searchkeywords_destroy
class SearchkeywordsApi(BaseApi):
    searchkeywords_retrieve = searchkeywords_retrieve.make_request
    searchkeywords_create = searchkeywords_create.make_request
    searchkeywords_retrieve_2 = searchkeywords_retrieve_2.make_request
    searchkeywords_update = searchkeywords_update.make_request
    searchkeywords_destroy = searchkeywords_destroy.make_request