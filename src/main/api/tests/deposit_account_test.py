import pytest

from src.main.api.generators.deposit_rule import DepositRule
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest

from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self, db_session: Session, api_manager: ApiManager,
                                   create_user_request: CreateUserRequest,
                                   account_response: CreateAccountResponse) -> None:
        deposit_account_request = DepositAccountRequest(
            accountId=account_response.id,
            amount=DepositRule.generate_valid_deposit_amount()
        )

        response = api_manager.user_steps.deposit_account(create_user_request, deposit_account_request)

        expected_balance = account_response.balance + deposit_account_request.amount
        assert response.id == account_response.id, (
            f"Ожидали ID счёта {account_response.id}, получили {response.id}"
        )

        assert response.balance == expected_balance, (
            f"Ожидали баланс счёта {expected_balance}, получили {response.balance}"
        )

        account_from_db = Account.get_account_by_id(db_session, response.id)

        assert account_from_db is not None, (
            f"Ожидали найти в БД счёт с ID {response.id}, но запись не найдена"
        )

        assert account_from_db.id == response.id, (
            f"Ожидали ID счёта в БД {response.id}, получили {account_from_db.id}"
        )

        assert account_from_db.balance is not None, (
            f"Ожидали заполненное поле balance у созданного счёта, получили None"
        )

        assert account_from_db.balance == expected_balance, (
            f"Ожидали баланс счета {expected_balance}, получили {account_from_db.balance}"
        )

    def test_deposit_account_invalid(self, db_session: Session, api_manager: ApiManager,
                                     create_user_request: CreateUserRequest,
                                     account_response: CreateAccountResponse) -> None:
        deposit_account_request = DepositAccountRequest(
            accountId=account_response.id,
            amount=DepositRule.generate_invalid_deposit_amount()
        )

        api_manager.user_steps.deposit_invalid_account(create_user_request, deposit_account_request)

        account_from_db = Account.get_account_by_id(db_session, account_response.id)

        assert account_from_db is not None, (
            f"Ожидали найти в БД счёт с ID {account_response.id}, но запись не найдена"
        )

        assert account_from_db.balance == account_response.balance, (
            f"Ожидали, что баланс счета останется {account_response.balance}, "
            f"получили {account_from_db.balance}"
        )
