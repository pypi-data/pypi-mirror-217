from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from feedancy_client.lib.base import BaseApi
from feedancy_client.lib.request import ApiRequest
from feedancy_client.lib import json
class Skill(BaseModel):
    id: int 
    name: str 

def make_request(self: BaseApi,


) -> Skill:
    

    
    body = None
    

    m = ApiRequest(
        method="GET",
        path="/skill/".format(
            
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
            
                "application/json": Skill,
            
        },
    
    }, m)