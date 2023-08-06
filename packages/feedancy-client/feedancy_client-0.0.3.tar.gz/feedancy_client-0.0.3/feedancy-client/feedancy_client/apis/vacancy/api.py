from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import vacancy_list
from . import vacancy_create
from . import vacancy_retrieve
from . import vacancy_update
from . import vacancy_destroy
class VacancyApi(BaseApi):
    vacancy_list = vacancy_list.make_request
    vacancy_create = vacancy_create.make_request
    vacancy_retrieve = vacancy_retrieve.make_request
    vacancy_update = vacancy_update.make_request
    vacancy_destroy = vacancy_destroy.make_request