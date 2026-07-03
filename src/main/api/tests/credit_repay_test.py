import pytest

from main.api.models.create_user_request import CreateUserRequest
from main.api.models.credit_repay_request import CreditRepayRequest
from main.api.models.credit_request_request import CreditRequestRequest
from main.api.requests.create_account_requester import CreateAccountRequester
from main.api.requests.create_user_requester import CreateUserRequester
from main.api.requests.credit_repay_requester import CreditRepayRequester
from main.api.requests.credit_request_requester import CreditRequestRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_valid(self):
        create_user_request = CreateUserRequest(username="Vika145", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()

        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1591", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        credit_request = CreditRequestRequest(accountId=account_response.id, amount=5000, termMonths=12)
        CreditRequestRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1591", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post(credit_request)

        credit_repay_request = CreditRepayRequest(creditId=credit_request.creditId, accountId=account_response.id,
                                                  amount=credit_request.amount)
        response = CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1591", password=""),
            response_spec=ResponseSpecs.request_ok()
        ).post(credit_repay_request)

        assert response.amountDeposited == credit_repay_request.amount
        assert response.creditId == credit_repay_request.creditId

    def test_credit_repay_invalid(self):
        create_user_request = CreateUserRequest(username="Vika145", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()

        ).post(create_user_request)

        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1591", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post()

        credit_request = CreditRequestRequest(accountId=account_response.id, amount=5000, termMonths=12)
        CreditRequestRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1591", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_create()
        ).post(credit_request)

        credit_repay_request = CreditRepayRequest(creditId=999, accountId=account_response.id,
                                                  amount=credit_request.amount)
        CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username="Vika1591", password=""),
            response_spec=ResponseSpecs.request_not_found()
        ).post(credit_repay_request)
