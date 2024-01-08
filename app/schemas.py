from pydantic import BaseModel, Field
from datetime import datetime

class ExpenseRequest(BaseModel):
    amount: float
    category: str
    description: str
    id: int
    username: str


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: str
    created_at: datetime = Field(..., description="Creation date in ISO format")
    username: str
    # updated_at: datetime = Field(..., description="Creation date in ISO format")


class UserSchema(BaseModel):
    username: str
    user_id: int
