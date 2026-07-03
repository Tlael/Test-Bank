import pytest

from main.api.models.create_user_request import CreateUserRequest
from main.api.models.deposit_account_request import DepositAccountRequest
from main.api.models.transfer_account_request import TransferAccountRequest
from main.api.requests.create_account_requester import CreateAccountRequester
from main.api.requests.create_user_requester import CreateUserRequester
from main.api.requests.deposit_account_requester import DepositAccountRequester
from main.api.requests.transfer_account_requester import TransferAccountRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(self):
        create_user_request = CreateUserRequest(username="Vika1579", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()

        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1579", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        deposit_account_request = DepositAccountRequest(accountId=account_response.id, amount=1000)
        response_deposit_id = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1579", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)

        transfer_account_request = TransferAccountRequest(fromAccountId=response_deposit_id.id, toAccountId=2,
                                                          amount=500)
        response = TransferAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1579", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_account_request)

        assert response.fromAccountId == response_deposit_id.id
        assert response.toAccountId == 2

    def test_transfer_account_invalid(self):
        create_user_request = CreateUserRequest(username="Vika1580", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()

        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1580", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        deposit_account_request = DepositAccountRequest(accountId=account_response.id, amount=1000)
        response_deposit_id = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1580", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)

        transfer_account_request = TransferAccountRequest(fromAccountId=response_deposit_id.id, toAccountId=2,
                                                          amount=499)
        TransferAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1580", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(transfer_account_request)
