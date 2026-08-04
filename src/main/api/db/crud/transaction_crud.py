from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction

class TransactionCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, credit_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(credit_id=credit_id).first()