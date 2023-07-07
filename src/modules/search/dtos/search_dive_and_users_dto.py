from pydantic import BaseModel

class SearchDiveAndUserDTO(BaseModel):
    search_value: str
    user_id: str