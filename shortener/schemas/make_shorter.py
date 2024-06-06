from pydantic import UUID4, BaseModel, Field, HttpUrl, validator
from url_normalize import url_normalize


class MakeShorterRequest(BaseModel):
    url: HttpUrl = Field(title="URL to be shortened")

    @classmethod
    @validator("url", allow_reuse=True, pre=True)
    def normalize_link(cls, link):
        return url_normalize(link)


class MakeShorterResponse(BaseModel):
    short_url: HttpUrl = Field(title="Shortened URL")
    secret_key: UUID4

    class Config:
        from_attributes = True
