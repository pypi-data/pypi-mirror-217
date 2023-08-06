from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import salary_retrieve
from . import salary_create
from . import salary_retrieve_2
from . import salary_update
from . import salary_destroy
class SalaryApi(BaseApi):
    salary_retrieve = salary_retrieve.make_request
    salary_create = salary_create.make_request
    salary_retrieve_2 = salary_retrieve_2.make_request
    salary_update = salary_update.make_request
    salary_destroy = salary_destroy.make_request