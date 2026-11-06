from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    ad_id: int
    sender_id: int
    receiver_id: int
    text: str


class MessageOut(MessageCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
