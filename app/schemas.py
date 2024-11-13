from pydantic import BaseModel
from typing import Optional

class SSHKeyCreate(BaseModel):
    description: Optional[str] = None

class SSHKeyResponse(BaseModel):
    id: int
    description: Optional[str]
    private_key: str
    public_key: str
    created_at: str
    message: str

    class Config:
        orm_mode = True
