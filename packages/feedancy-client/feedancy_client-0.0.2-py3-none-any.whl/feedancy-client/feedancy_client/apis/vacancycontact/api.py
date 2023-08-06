from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import vacancycontact_retrieve
from . import vacancycontact_create
from . import vacancycontact_retrieve_2
from . import vacancycontact_update
from . import vacancycontact_destroy
class VacancycontactApi(BaseApi):
    vacancycontact_retrieve = vacancycontact_retrieve.make_request
    vacancycontact_create = vacancycontact_create.make_request
    vacancycontact_retrieve_2 = vacancycontact_retrieve_2.make_request
    vacancycontact_update = vacancycontact_update.make_request
    vacancycontact_destroy = vacancycontact_destroy.make_request