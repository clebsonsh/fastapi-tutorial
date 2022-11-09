from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    published: bool | None = True


class ShowBLog(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True
