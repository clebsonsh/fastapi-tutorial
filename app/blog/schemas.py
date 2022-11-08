from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    published: bool | None = True
