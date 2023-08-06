from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from feedancy_client.lib.base import BaseApi
from feedancy_client.lib.request import ApiRequest
from feedancy_client.lib import json
class VacancySkill(BaseModel):
    id: int 
    skill: int 
    vacancy: int 

def make_request(self: BaseApi,


) -> VacancySkill:
    

    
    body = None
    

    m = ApiRequest(
        method="GET",
        path="/vacancyskill/".format(
            
        ),
        content_type=None,
        body=body,
        headers=self._only_provided({
        }),
        query_params=self._only_provided({
        }),
        cookies=self._only_provided({
        }),
    )
    return self.make_request({
    
        "200": {
            
                "application/json": VacancySkill,
            
        },
    
    }, m)