import pytest

from main.api.models.create_user_request import CreateUserRequest
from main.api.models.deposit_account_request import DepositAccountRequest
from main.api.requests.create_account_requester import CreateAccountRequester
from main.api.requests.create_user_requester import CreateUserRequester
from main.api.requests.deposit_account_requester import DepositAccountRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self):
        create_user_request = CreateUserRequest(username="Vika1577", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec = RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec = ResponseSpecs.request_ok()

        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec = RequestSpecs.auth_headers(username="Vika1577", password="Pas!sw0rd"),
            response_spec = ResponseSpecs.request_create()
        ).post()

        deposit_account_request = DepositAccountRequest(accountId=account_response.id, amount=1000)
        response = DepositAccountRequester(
            request_spec = RequestSpecs.auth_headers(username="Vika1577", password="Pas!sw0rd"),
            response_spec = ResponseSpecs.request_ok()
        ).post(deposit_account_request)

        assert response.id == account_response.id
        assert response.balance == 1000

    def test_deposit_account_invalid(self):
        create_user_request = CreateUserRequest(username="Vika1578", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()

        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1578", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        deposit_account_request = DepositAccountRequest(accountId=account_response.id, amount=999)
        DepositAccountRequester(
            request_spec = RequestSpecs.auth_headers(username="Vika1578", password="Pas!sw0rd"),
            response_spec = ResponseSpecs.request_bad()
        ).post(deposit_account_request)