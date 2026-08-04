from src.main.api.models.base_model import BaseModel


class CreditRequestResponse(BaseModel):
    accountId: int
    amount: float
    termMonths: int
    balance: float
    creditId: int
