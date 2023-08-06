from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from feedancy_client.lib.base import BaseApi
from feedancy_client.lib.request import ApiRequest
from feedancy_client.lib import json
class SearchKeywords(BaseModel):
    name: str 

def make_request(self: BaseApi,

    __request__: SearchKeywords,


) -> SearchKeywords:
    

    
    body = __request__
    

    m = ApiRequest(
        method="POST",
        path="/searchkeywords/".format(
            
        ),
        content_type="application/json",
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
            
                "application/json": SearchKeywords,
            
        },
    
    }, m)