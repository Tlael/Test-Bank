import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
    )
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest,
                               db_session: Session) -> None:
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username, (
            f"Ожидали username {create_user_request.username}, "
            f"получили {response.username}"
        )

        assert create_user_request.role == response.role, (
            f"Ожидали роль {create_user_request.role}, "
            f"получили {response.role}"
        )

        user_from_db = User.get_user_by_username(
            db_session,
            create_user_request.username,
        )

        assert user_from_db is not None, (
            f"Ожидали найти пользователя {create_user_request.username} в БД, "
            "но запись не найдена"
        )

        assert user_from_db.username == create_user_request.username, (
            f"Ожидали username в БД {create_user_request.username}, "
            f"получили {user_from_db.username}"
        )

    @pytest.mark.parametrize(
        "username, password",
        [
            ("aбв", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("Vika1", "Pas!sw0rд"),
            ("Vika2", "Pas!sw0"),
            ("Vika3", "pas!sw0rd"),
            ("Vika4", "PAS!SW0RD"),
            ("Vika5", "Passsw0rd"),
            ("Vika6", "Pas!sword"),

        ]
    )
    def test_create_user_invalid(self, db_session: Session, username: str, password: str, api_manager: ApiManager) -> None:
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is None, (
            f"Ожидали, что пользователь {create_user_request.username} "
            "не будет создан, но запись найдена в БД"
        )