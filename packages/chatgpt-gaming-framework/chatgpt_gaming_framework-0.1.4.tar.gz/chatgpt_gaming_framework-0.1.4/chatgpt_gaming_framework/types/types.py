import pydantic
from typing import List

class Conversation(pydantic.BaseModel):
    role: str
    content: str = None
    name: str = None # needed for functions
    function_call: dict = None

class ConversationList(pydantic.BaseModel):
    conversations: List[Conversation]