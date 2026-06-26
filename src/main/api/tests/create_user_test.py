import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self):
        create_user_request = CreateUserRequest(username="Vika235", password="Pas!sw0rd", role="ROLE_USER")

        response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()

        ).post(create_user_request)

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
    def test_create_user_invalid(self, username, password):

        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_bad()
        ).post(create_user_request)
