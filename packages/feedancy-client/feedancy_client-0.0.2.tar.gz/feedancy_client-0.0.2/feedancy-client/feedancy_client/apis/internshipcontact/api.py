from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import internshipcontact_retrieve
from . import internshipcontact_create
from . import internshipcontact_retrieve_2
from . import internshipcontact_update
from . import internshipcontact_destroy
class InternshipcontactApi(BaseApi):
    internshipcontact_retrieve = internshipcontact_retrieve.make_request
    internshipcontact_create = internshipcontact_create.make_request
    internshipcontact_retrieve_2 = internshipcontact_retrieve_2.make_request
    internshipcontact_update = internshipcontact_update.make_request
    internshipcontact_destroy = internshipcontact_destroy.make_request