import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, db_session: Session, api_manager: ApiManager,
                            create_user_request: CreateUserRequest) -> None:
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0, (
            f"Ожидали начальный баланс счёта 0, получили {response.balance}"
        )

        account_from_db = Account.get_account_by_id(
            db_session,
            response.id,
        )

        assert account_from_db is not None, (
            f"Ожидали найти в БД счёт с ID {response.id}, но запись не найдена"
        )

        assert account_from_db.id == response.id, (
            f"Ожидали ID счёта в БД {response.id}, получили {account_from_db.id}"
        )

        assert account_from_db.balance is not None, (
            "Ожидали заполненное поле balance у созданного счёта, получили None"
        )
