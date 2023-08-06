from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import internship_retrieve
from . import internship_create
from . import internship_retrieve_2
from . import internship_update
from . import internship_destroy
class InternshipApi(BaseApi):
    internship_retrieve = internship_retrieve.make_request
    internship_create = internship_create.make_request
    internship_retrieve_2 = internship_retrieve_2.make_request
    internship_update = internship_update.make_request
    internship_destroy = internship_destroy.make_request