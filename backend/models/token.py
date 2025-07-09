from pydantic import BaseModel
from typing import Union

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Union[int, None] = None
    username: Union[str, None] = None