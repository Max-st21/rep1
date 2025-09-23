from pydantic import BaseModel, constr
from typing import Optional

class Route(BaseModel):
    user_id: int
    route_name: constr(min_length=1, max_length=30)
    description: Optional[str] = None
    route_parametrs: dict

class Route_place(BaseModel):
    place_id: list[int]

class User_interests(BaseModel):
    user_id: int
    category_id: list[int]

class Route_param(BaseModel):
    route_parametrs: dict
