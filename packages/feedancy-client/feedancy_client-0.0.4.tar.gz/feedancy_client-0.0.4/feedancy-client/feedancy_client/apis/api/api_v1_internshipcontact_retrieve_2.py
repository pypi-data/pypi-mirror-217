from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from feedancy_client.lib.base import BaseApi
from feedancy_client.lib.request import ApiRequest
from feedancy_client.lib import json
class InternshipContact(BaseModel):
    contact: int 
    id: int 
    internship: int 

def make_request(self: BaseApi,


    id: str,

) -> InternshipContact:
    

    
    body = None
    

    m = ApiRequest(
        method="GET",
        path="/api/v1/internshipcontact/{id}/".format(
            
                id=id,
            
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
            
                "application/json": InternshipContact,
            
        },
    
    }, m)