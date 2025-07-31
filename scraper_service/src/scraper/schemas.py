from datetime import datetime
from pydantic import BaseModel



class WorkSchema(BaseModel):
    id: int | None = None
    source: str
    url: str
    title: str
    content: str
    remote: str
    company: str
    time: str
    eng_level: str | None = None
    tags: list[str]
    salary: int | None = None 
    published_at: datetime
    company_link: str | None = None




