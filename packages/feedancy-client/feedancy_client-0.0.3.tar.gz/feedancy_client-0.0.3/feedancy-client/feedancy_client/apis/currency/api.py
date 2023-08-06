from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import currency_retrieve
from . import currency_create
from . import currency_retrieve_2
from . import currency_update
from . import currency_destroy
class CurrencyApi(BaseApi):
    currency_retrieve = currency_retrieve.make_request
    currency_create = currency_create.make_request
    currency_retrieve_2 = currency_retrieve_2.make_request
    currency_update = currency_update.make_request
    currency_destroy = currency_destroy.make_request