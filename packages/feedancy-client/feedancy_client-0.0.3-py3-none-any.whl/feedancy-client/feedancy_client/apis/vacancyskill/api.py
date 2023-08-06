from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import vacancyskill_retrieve
from . import vacancyskill_create
from . import vacancyskill_retrieve_2
from . import vacancyskill_update
from . import vacancyskill_destroy
class VacancyskillApi(BaseApi):
    vacancyskill_retrieve = vacancyskill_retrieve.make_request
    vacancyskill_create = vacancyskill_create.make_request
    vacancyskill_retrieve_2 = vacancyskill_retrieve_2.make_request
    vacancyskill_update = vacancyskill_update.make_request
    vacancyskill_destroy = vacancyskill_destroy.make_request