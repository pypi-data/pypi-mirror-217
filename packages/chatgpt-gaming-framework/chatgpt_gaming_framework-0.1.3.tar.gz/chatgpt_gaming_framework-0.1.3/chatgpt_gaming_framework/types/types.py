import pydantic
from typing import List

class Conversation(pydantic.BaseModel):
    role: str
    content: str
    name: str = None # needed for functions
    function_call: dict = None

class ConversationList(pydantic.BaseModel):
    conversations: List[Conversation]