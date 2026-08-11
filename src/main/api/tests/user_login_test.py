import pytest

from src.main.api.configs.config import Config
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager) -> None:
        login_user_request = LoginUserRequest(
            username=Config.fetch("adminUsername"),
            password=Config.fetch("adminPassword"),
        )
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username, (
            f"Ожидали username {login_user_request.username}, "
            f"получили {response.user.username}"
        )

        assert response.user.role == "ROLE_ADMIN", (
            f"Ожидали роль ROLE_ADMIN, получили {response.user.role}"
        )

    def test_login_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest) -> None:
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, (
            f"Ожидали username {create_user_request.username}, "
            f"получили {response.user.username}"
        )

        assert response.user.role == "ROLE_USER", (
            f"Ожидали роль ROLE_USER, получили {response.user.role}"
        )
