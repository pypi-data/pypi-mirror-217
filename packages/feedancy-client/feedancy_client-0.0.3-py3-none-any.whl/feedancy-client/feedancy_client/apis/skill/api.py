from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import skill_retrieve
from . import skill_create
from . import skill_retrieve_2
from . import skill_update
from . import skill_destroy
class SkillApi(BaseApi):
    skill_retrieve = skill_retrieve.make_request
    skill_create = skill_create.make_request
    skill_retrieve_2 = skill_retrieve_2.make_request
    skill_update = skill_update.make_request
    skill_destroy = skill_destroy.make_request