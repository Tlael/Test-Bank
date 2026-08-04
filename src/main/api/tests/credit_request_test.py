import pytest
from pydantic import ValidationError

from src.main.api.models.credit_request_request import CreditRequestRequest


@pytest.mark.api
class TestCreditRequest:

    @pytest.mark.xfail(
        reason=(
                "Known API contract defect: /credit/request returns 'id' "
                "instead of Swagger field 'accountId'"
        ),
        raises=ValidationError,
        strict=True,
    )
    def test_credit_request_valid(self, api_manager, create_credit_user_request):
        account_response = api_manager.user_steps.create_account(create_credit_user_request)

        credit_request = CreditRequestRequest(
            accountId=account_response.id,
            amount=5000,
            termMonths=12
        )

        response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)

        assert response.amount == 5000
        assert response.termMonths == 12

    @pytest.mark.xfail(
        reason=(
                "Known API contract defect: Swagger declares 422 for credit amount "
                "above 15000, but API returns a different status code"
        ),
        raises=AssertionError,
        strict=True,
    )
    def test_credit_request_invalid(self, api_manager, create_credit_user_request):
        account_response = api_manager.user_steps.create_account(create_credit_user_request)

        credit_request = CreditRequestRequest(
            accountId=account_response.id,
            amount=20000,
            termMonths=12
        )

        api_manager.user_steps.credit_invalid_request(create_credit_user_request, credit_request)
