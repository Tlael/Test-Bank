import pytest

from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest


@pytest.mark.api
class TestCreditRepay:
    @pytest.mark.xfail
    def test_credit_repay_valid(self, api_manager, create_credit_user_request):
        account_response = api_manager.user_steps.create_account(create_credit_user_request)

        credit_request = CreditRequestRequest(
            accountId=account_response.id,
            amount=5000,
            termMonths=12
        )

        credit_response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)

        credit_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=account_response.id,
            amount=5000
        )

        response = api_manager.user_steps.credit_repay_request(create_credit_user_request, credit_repay_request)

        assert response.amountDeposited == credit_repay_request.amount
        assert response.creditId == credit_response.creditId

    @pytest.mark.xfail
    def test_credit_repay_invalid(self, api_manager, create_credit_user_request):
        account_response = api_manager.user_steps.create_account(create_credit_user_request)

        credit_request = CreditRequestRequest(
            accountId=account_response.id,
            amount=5000,
            termMonths=12
        )

        credit_response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)

        credit_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=account_response.id,
            amount=1000000
        )

        api_manager.user_steps.credit_invalid_repay(create_credit_user_request, credit_repay_request)
