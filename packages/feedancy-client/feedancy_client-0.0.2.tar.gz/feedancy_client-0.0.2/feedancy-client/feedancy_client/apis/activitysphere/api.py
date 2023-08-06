from __future__ import annotations

from feedancy_client.lib.base import BaseApi

from . import activitysphere_retrieve
from . import activitysphere_create
from . import activitysphere_retrieve_2
from . import activitysphere_update
from . import activitysphere_destroy
class ActivitysphereApi(BaseApi):
    activitysphere_retrieve = activitysphere_retrieve.make_request
    activitysphere_create = activitysphere_create.make_request
    activitysphere_retrieve_2 = activitysphere_retrieve_2.make_request
    activitysphere_update = activitysphere_update.make_request
    activitysphere_destroy = activitysphere_destroy.make_request