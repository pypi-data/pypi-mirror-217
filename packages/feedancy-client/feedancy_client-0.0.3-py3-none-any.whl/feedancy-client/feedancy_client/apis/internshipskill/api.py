from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import internshipskill_retrieve
from . import internshipskill_create
from . import internshipskill_retrieve_2
from . import internshipskill_update
from . import internshipskill_destroy
class InternshipskillApi(BaseApi):
    internshipskill_retrieve = internshipskill_retrieve.make_request
    internshipskill_create = internshipskill_create.make_request
    internshipskill_retrieve_2 = internshipskill_retrieve_2.make_request
    internshipskill_update = internshipskill_update.make_request
    internshipskill_destroy = internshipskill_destroy.make_request