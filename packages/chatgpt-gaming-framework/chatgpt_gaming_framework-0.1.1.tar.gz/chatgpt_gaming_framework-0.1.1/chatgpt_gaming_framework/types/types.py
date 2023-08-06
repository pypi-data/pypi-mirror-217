import pydantic
from typing import List

class Conversation(pydantic.BaseModel):
    role: str
    content: str
    name: str = None # needed for functions

class ConversationList(pydantic.BaseModel):
    conversations: List[Conversation]