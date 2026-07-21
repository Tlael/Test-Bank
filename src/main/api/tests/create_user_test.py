import pytest

from main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
    )
    def test_create_user_valid(self, api_manager, create_user_request):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

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
    def test_create_user_invalid(self, username, password, api_manager):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)
