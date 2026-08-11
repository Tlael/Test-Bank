import pytest
from pydantic import ValidationError

from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest


@pytest.mark.api
class TestCreditRepay:
    @pytest.mark.xfail(
        reason=(
                "Blocked by known /credit/request contract defect: API returns 'id' "
                "instead of Swagger field 'accountId'"
        ),
        raises=ValidationError,
        strict=True,
    )
    def test_credit_repay_valid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                valid_credit_repay_request: CreditRepayRequest) -> None:
        response = api_manager.user_steps.credit_repay_request(create_credit_user_request, valid_credit_repay_request)

        assert response.amountDeposited == valid_credit_repay_request.amount, (
            f"Ожидали сумму погашения {valid_credit_repay_request.amount}, "
            f"получили {response.amountDeposited}"
        )

        assert response.creditId == valid_credit_repay_request.creditId, (
            f"Ожидали ID кредита {valid_credit_repay_request.creditId}, "
            f"получили {response.creditId}"
        )

    @pytest.mark.xfail(
        reason=(
                "Blocked by known /credit/request contract defect: API returns 'id' "
                "instead of Swagger field 'accountId'"
        ),
        raises=ValidationError,
        strict=True,
    )
    def test_credit_repay_invalid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                  invalid_credit_repay_request: CreditRepayRequest) -> None:
        api_manager.user_steps.credit_invalid_repay(create_credit_user_request, invalid_credit_repay_request)
