from pydantic import BaseModel, EmailStr, Field

class AudienceBase(BaseModel):
    email: EmailStr
    segment: str = Field(..., min_length=2, max_length=50)

class AudienceCreate(AudienceBase):
    pass

class AudienceResponse(AudienceBase):
    id: int

    class Config:
        orm_mode = True
