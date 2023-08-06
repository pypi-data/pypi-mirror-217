from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import company_retrieve
from . import company_create
from . import company_retrieve_2
from . import company_update
from . import company_destroy
class CompanyApi(BaseApi):
    company_retrieve = company_retrieve.make_request
    company_create = company_create.make_request
    company_retrieve_2 = company_retrieve_2.make_request
    company_update = company_update.make_request
    company_destroy = company_destroy.make_request