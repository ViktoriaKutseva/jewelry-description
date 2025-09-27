# Value objects for the jewelry domain
from pydantic import BaseModel, Field


class Money(BaseModel):
    amount: float = Field(..., ge=0)
    currency: str = "KZT"

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"
