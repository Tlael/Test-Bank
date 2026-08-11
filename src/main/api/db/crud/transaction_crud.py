from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction

class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_credit_id(
        db: Session,
        credit_id: int,
    ) -> Transaction | None:
        return db.query(Transaction).filter_by(
            credit_id=credit_id
        ).first()

    @staticmethod
    def get_transaction_by_accounts(
        db: Session,
        from_account_id: int,
        to_account_id: int,
    ) -> Transaction | None:
        return db.query(Transaction).filter_by(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
        ).first()