import pytest
from sqlalchemy.orm import Session

from src.main.api.generators.transfer_rule import TransferRule
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(self, db_session: Session, api_manager: ApiManager,
                                    create_user_request: CreateUserRequest, accounts_for_transfer: tuple[
                CreateAccountResponse,
                CreateAccountResponse,
                DepositAccountRequest], ) -> None:
        first_account, second_account, deposit_request = accounts_for_transfer
        transfer_amount = TransferRule.generate_valid_transfer_amount(deposit_request.amount)

        transfer_request = TransferAccountRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=transfer_amount
        )

        response = api_manager.user_steps.transfer_account(create_user_request, transfer_request)

        expected_first_balance = deposit_request.amount - transfer_amount
        expected_second_balance = second_account.balance + transfer_amount

        assert response.fromAccountId == first_account.id, (
            f"Ожидали ID счёта отправителя {first_account.id}, "
            f"получили {response.fromAccountId}"
        )

        assert response.toAccountId == second_account.id, (
            f"Ожидали ID счёта получателя {second_account.id}, "
            f"получили {response.toAccountId}"
        )

        assert response.fromAccountIdBalance == expected_first_balance, (
            f"Ожидали остаток на счёте отправителя {expected_first_balance}, "
            f"получили {response.fromAccountIdBalance}"
        )

        first_account_from_db = Account.get_account_by_id(
            db_session,
            first_account.id
        )

        second_account_from_db = Account.get_account_by_id(
            db_session,
            second_account.id
        )

        transaction_from_db = Transaction.get_transaction_by_accounts(db_session, first_account.id, second_account.id)

        assert first_account_from_db is not None, (
            f"Ожидали найти в БД счёт отправителя {first_account.id}, но запись не найдена"
        )

        assert second_account_from_db is not None, (
            f"Ожидали найти в БД счёт получателя {second_account.id}, но запись не найдена"
        )

        assert transaction_from_db is not None, (
            f"Ожидали найти транзакцию из счёта {first_account.id} "
            f"в счёт {second_account.id}, но запись не найдена"
        )

        assert first_account_from_db.balance == expected_first_balance, (
            f"Ожидали баланс счёта отправителя {expected_first_balance}, "
            f"получили {first_account_from_db.balance}"
        )

        assert second_account_from_db.balance == expected_second_balance, (
            f"Ожидали баланс счёта получателя {expected_second_balance}, "
            f"получили {second_account_from_db.balance}"
        )

        assert transaction_from_db.from_account_id == first_account.id, (
            f"Ожидали ID счёта отправителя {first_account.id}, "
            f"получили {transaction_from_db.from_account_id}"
        )

        assert transaction_from_db.to_account_id == second_account.id, (
            f"Ожидали ID счёта получателя {second_account.id}, "
            f"получили {transaction_from_db.to_account_id}"
        )

        assert transaction_from_db.amount == transfer_amount, (
            f"Ожидали сумму перевода {transfer_amount}, "
            f"получили {transaction_from_db.amount}"
        )

    def test_transfer_account_invalid(self, db_session: Session, api_manager: ApiManager,
                                      create_user_request: CreateUserRequest,
                                      accounts_for_transfer: tuple[
                                          CreateAccountResponse,
                                          CreateAccountResponse,
                                          DepositAccountRequest,
                                      ], ) -> None:
        first_account, second_account, deposit_request = accounts_for_transfer

        transfer_request = TransferAccountRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=TransferRule.generate_invalid_transfer_amount()
        )

        api_manager.user_steps.transfer_invalid_account(create_user_request, transfer_request)

        first_account_from_db = Account.get_account_by_id(
            db_session,
            first_account.id
        )

        second_account_from_db = Account.get_account_by_id(
            db_session,
            second_account.id
        )

        transaction_from_db = Transaction.get_transaction_by_accounts(
            db_session,
            first_account.id,
            second_account.id,
        )

        assert first_account_from_db is not None, (
            f"Ожидали найти в БД счёт отправителя {first_account.id}, но запись не найдена"
        )

        assert second_account_from_db is not None, (
            f"Ожидали найти в БД счёт получателя {second_account.id}, но запись не найдена"
        )

        assert transaction_from_db is None, (
            f"Ожидали не найти транзакцию из счёта {first_account.id} "
            f"в счёт {second_account.id}, но запись найдена"
        )

        assert first_account_from_db.balance == deposit_request.amount, (
            f"Ожидали баланс счёта отправителя {deposit_request.amount}, "
            f"получили {first_account_from_db.balance}"
        )

        assert second_account_from_db.balance == second_account.balance, (
            f"Ожидали баланс счёта получателя {second_account.balance}, "
            f"получили {second_account_from_db.balance}"
        )
