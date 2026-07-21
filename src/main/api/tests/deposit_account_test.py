import pytest

from main.api.models.deposit_account_request import DepositAccountRequest


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self, api_manager, create_user_request, account_response):

        deposit_account_request = DepositAccountRequest(
            accountId=account_response.id,
            amount=1000
        )

        response = api_manager.user_steps.deposit_account(create_user_request, deposit_account_request)

        assert response.id == account_response.id
        assert response.balance == 1000

    def test_deposit_account_invalid(self, api_manager, create_user_request, account_response):

        deposit_account_request = DepositAccountRequest(
            accountId=account_response.id,
            amount=999
        )

        api_manager.user_steps.deposit_invalid_account(create_user_request, deposit_account_request)
