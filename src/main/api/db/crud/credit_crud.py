from sqlalchemy.orm import Session
from src.main.api.db.models.credit_table import Credit


class CreditCrudDb:
    @staticmethod
    def get_credit_by_amount(db: Session, id: int) -> Credit | None:
        return db.query(Credit).filter_by(id=id).first()