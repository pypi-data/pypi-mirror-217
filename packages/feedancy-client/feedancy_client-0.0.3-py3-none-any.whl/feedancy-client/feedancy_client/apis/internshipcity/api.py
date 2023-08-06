from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import internshipcity_retrieve
from . import internshipcity_create
from . import internshipcity_retrieve_2
from . import internshipcity_update
from . import internshipcity_destroy
class InternshipcityApi(BaseApi):
    internshipcity_retrieve = internshipcity_retrieve.make_request
    internshipcity_create = internshipcity_create.make_request
    internshipcity_retrieve_2 = internshipcity_retrieve_2.make_request
    internshipcity_update = internshipcity_update.make_request
    internshipcity_destroy = internshipcity_destroy.make_request