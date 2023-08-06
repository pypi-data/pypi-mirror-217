from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import vacancycity_retrieve
from . import vacancycity_create
from . import vacancycity_retrieve_2
from . import vacancycity_update
from . import vacancycity_destroy
class VacancycityApi(BaseApi):
    vacancycity_retrieve = vacancycity_retrieve.make_request
    vacancycity_create = vacancycity_create.make_request
    vacancycity_retrieve_2 = vacancycity_retrieve_2.make_request
    vacancycity_update = vacancycity_update.make_request
    vacancycity_destroy = vacancycity_destroy.make_request