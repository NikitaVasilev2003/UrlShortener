from pydantic import UUID4, BaseModel, Field, HttpUrl, field_validator
from url_normalize import url_normalize

class MakeShorterRequest(BaseModel):
    url: HttpUrl = Field(title="URL to be shortened")
    vip_key: str | None = Field(default=None, title="Custom short URL key")
    time_to_live: int | None = Field(default=1, title="Time to live")
    time_to_live_unit: str | None = Field(default="DAYS", title="Unit for time to live")

    @field_validator("url", mode="before")
    def normalize_link(cls, link):
        return url_normalize(link)

class MakeShorterResponse(BaseModel):
    short_url: HttpUrl = Field(title="Shortened URL")
    secret_key: UUID4

    class Config:
        from_attributes = True

