import pytest

from src.main.api.models.transfer_account_request import TransferAccountRequest


@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(self, api_manager, create_user_request, accounts_for_transfer):
        first_account, second_account = accounts_for_transfer
        transfer_amount = 500

        transfer_request = TransferAccountRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=transfer_amount
        )

        response = api_manager.user_steps.transfer_account(create_user_request, transfer_request)

        assert response.fromAccountId == first_account.id
        assert response.toAccountId == second_account.id
        assert response.fromAccountIdBalance == 1000 - transfer_amount

    def test_transfer_account_invalid(self, api_manager, create_user_request, accounts_for_transfer):
        first_account, second_account = accounts_for_transfer

        transfer_request = TransferAccountRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=499
        )

        api_manager.user_steps.transfer_invalid_account(create_user_request, transfer_request)
