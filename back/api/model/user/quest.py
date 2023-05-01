from pydantic import BaseModel


class CurrentQuestProgress(BaseModel):
    numerator: int = 0
    denominator: int = 0
