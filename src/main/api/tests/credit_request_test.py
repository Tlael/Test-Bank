import pytest

from main.api.models.create_user_request import CreateUserRequest
from main.api.models.credit_request_request import CreditRequestRequest
from main.api.requests.create_account_requester import CreateAccountRequester
from main.api.requests.create_user_requester import CreateUserRequester
from main.api.requests.credit_request_requester import CreditRequestRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreditRequest:
    @pytest.mark.xfail
    def test_credit_request_valid(self):
        create_user_request = CreateUserRequest(username="Vika1591", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()

        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1591", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        credit_request = CreditRequestRequest(accountId=account_response.id, amount=5000, termMonths=12)
        response = CreditRequestRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1591", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post(credit_request)

        assert response.amount == 5000
        assert response.termMonths == 12

    def test_credit_request_invalid(self):
        create_user_request = CreateUserRequest(username="Vika1595", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()

        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1595", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        credit_request = CreditRequestRequest(accountId=account_response.id, amount=20000, termMonths=12)
        CreditRequestRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1595", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(credit_request)
