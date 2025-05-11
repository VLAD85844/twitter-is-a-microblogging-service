from typing import Optional, List
from pydantic import BaseModel

class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None

class TweetOut(BaseModel):
    id: int
    content: str
    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class LikeOut(BaseModel):
    result: bool

