import pytest
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


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
    def test_credit_request_valid(self, db_session: Session, api_manager: ApiManager,
                                  create_credit_user_request: CreateCreditUserRequest,
                                  valid_credit_request: CreditRequestRequest) -> None:
        try:
            response = api_manager.user_steps.credit_request(create_credit_user_request, valid_credit_request)

        except ValidationError:
            credit_from_db = Credit.get_credit_by_account_id(
                db_session,
                valid_credit_request.accountId,
            )

            assert credit_from_db is not None, (
                f"Ожидали найти кредит для счёта {valid_credit_request.accountId}, "
                "но запись не найдена"
            )

            assert credit_from_db.account_id == valid_credit_request.accountId, (
                f"Ожидали ID счёта в БД {valid_credit_request.accountId}, получили {credit_from_db.account_id}"
            )

            assert credit_from_db.amount == valid_credit_request.amount, (
                f"Ожидали сумму кредита в БД {valid_credit_request.amount}, получили {credit_from_db.amount}"
            )

            assert credit_from_db.term_months == valid_credit_request.termMonths, (
                f"Ожидали срок кредита в БД {valid_credit_request.termMonths}, получили {credit_from_db.term_months}"
            )

            raise

        assert response.amount == valid_credit_request.amount, (
            f"Ожидали сумму кредита {valid_credit_request.amount}, "
            f"получили {response.amount}"
        )

        assert response.termMonths == valid_credit_request.termMonths, (
            f"Ожидали срок кредита {valid_credit_request.termMonths} месяцев, "
            f"получили {response.termMonths}"
        )

    @pytest.mark.xfail(
        reason=(
                "Known API contract defect: Swagger allows credit amount below 5000, "
                "but API rejects it with 400"
        ),
        raises=AssertionError,
        strict=True,
    )
    def test_credit_request_contract_valid_amount(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_credit_user_request: CreateCreditUserRequest,
            contract_valid_credit_request: CreditRequestRequest,
    ) -> None:
        try:
            api_manager.user_steps.credit_request(create_credit_user_request, contract_valid_credit_request)
        except AssertionError:
            credit_from_db = Credit.get_credit_by_account_id(
                db_session,
                contract_valid_credit_request.accountId,
            )

            assert credit_from_db is None, (
                f"Ожидали не найти кредит для счёта "
                f"{contract_valid_credit_request.accountId}, но запись найдена"
            )

            raise

    @pytest.mark.xfail(
        reason=(
                "Known API contract defect: Swagger declares 422 for credit amount "
                "above 15000, but API returns a different status code"
        ),
        raises=AssertionError,
        strict=True,
    )
    def test_credit_request_invalid(self, db_session: Session, api_manager: ApiManager,
                                    create_credit_user_request: CreateCreditUserRequest,
                                    invalid_credit_request: CreditRequestRequest) -> None:
        try:
            api_manager.user_steps.credit_invalid_request(create_credit_user_request, invalid_credit_request)

        except AssertionError:
            credit_from_db = Credit.get_credit_by_account_id(
                db_session,
                invalid_credit_request.accountId,
            )

            assert credit_from_db is None, (
                f"Ожидали не найти кредит для счёта {invalid_credit_request.accountId}, "
                "но запись найдена"
            )
            raise
