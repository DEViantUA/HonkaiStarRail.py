from pydantic import BaseModel
from datetime import datetime
from typing import List


class ImageGacha(BaseModel):
    icon: str
    full: str

class JumpRecord(BaseModel):
    uid: int
    id: int
    name: str
    rank: str
    count: int
    type: str
    time: datetime
    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True


class JumpRecordGacha(BaseModel):
    uid: int
    id: int
    name: str
    rank: str
    count: int
    type: str
    time: datetime
    dropped: int
    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True


class TotalTypeOne(BaseModel):
    name: str
    count: int

class Gacha(BaseModel):
    total: int
    total_rank_four: int
    total_rank_five: int
    next_four_garant: int
    next_five_garant: int
    total_type_one: List[TotalTypeOne]
    history: list

class URLParams(BaseModel):
    authkey_ver: int = None
    auth_appid: str = None
    gacha_id: str = None
    timestamp: int = None
    region: str = None
    default_gacha_type: int = None
    lang: str = None
    authkey: str = None
    game_biz: str = None
    page: int = None
    size: int = None
    gacha_type: int = None
    end_id: int = None