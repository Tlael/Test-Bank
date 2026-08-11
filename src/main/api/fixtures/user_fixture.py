import pytest

from src.main.api.generators.deposit_rule import DepositRule
from src.main.api.generators.credit_rule import CreditRule
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.credit_request_response import CreditRequestResponse


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_credit_user_request(api_manager):
    credit_user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_user(credit_user_request)

    return credit_user_request


@pytest.fixture
def account_response(api_manager, create_user_request):
    return api_manager.user_steps.create_account(
        create_user_request
    )


@pytest.fixture
def accounts_for_transfer(api_manager, create_user_request):
    first_account = api_manager.user_steps.create_account(
        create_user_request
    )

    second_account = api_manager.user_steps.create_account(
        create_user_request
    )

    deposit_request = DepositAccountRequest(
        accountId=first_account.id,
        amount=DepositRule.generate_valid_deposit_amount()
    )

    api_manager.user_steps.deposit_account(
        create_user_request,
        deposit_request
    )

    return first_account, second_account, deposit_request


@pytest.fixture
def valid_credit_request(api_manager: ApiManager,
                         create_credit_user_request: CreateCreditUserRequest) -> CreditRequestRequest:
    account_response = api_manager.user_steps.create_account(
        create_credit_user_request
    )
    credit_request = CreditRequestRequest(
        accountId=account_response.id,
        amount=CreditRule.generate_working_credit_amount(),
        termMonths=CreditRule.generate_valid_term_months()
    )
    return credit_request


@pytest.fixture
def invalid_credit_request(api_manager: ApiManager,
                           create_credit_user_request: CreateCreditUserRequest) -> CreditRequestRequest:
    account_response = api_manager.user_steps.create_account(create_credit_user_request)
    credit_request = CreditRequestRequest(
        accountId=account_response.id,
        amount=CreditRule.generate_working_credit_amount(),
        termMonths=CreditRule.generate_valid_term_months()
    )
    return credit_request


@pytest.fixture
def active_credit(
        api_manager: ApiManager,
        create_credit_user_request: CreateCreditUserRequest,
) -> tuple[CreateAccountResponse, CreditRequestResponse]:
    account_response = api_manager.user_steps.create_account(
        create_credit_user_request
    )

    credit_request = CreditRequestRequest(
        accountId=account_response.id,
        amount=CreditRule.generate_working_credit_amount(),
        termMonths=CreditRule.generate_valid_term_months(),
    )

    credit_response = api_manager.user_steps.credit_request(
        create_credit_user_request,
        credit_request,
    )

    return account_response, credit_response


@pytest.fixture
def valid_credit_repay_request(
        active_credit: tuple[CreateAccountResponse, CreditRequestResponse],
) -> CreditRepayRequest:
    account_response, credit_response = active_credit

    return CreditRepayRequest(
        creditId=credit_response.creditId,
        accountId=account_response.id,
        amount=credit_response.balance,
    )


@pytest.fixture
def invalid_credit_repay_request(
        active_credit: tuple[CreateAccountResponse, CreditRequestResponse],
) -> CreditRepayRequest:
    account_response, credit_response = active_credit

    return CreditRepayRequest(
        creditId=credit_response.creditId,
        accountId=account_response.id,
        amount=credit_response.balance + 1,
    )


@pytest.fixture
def contract_valid_credit_request(
        api_manager: ApiManager,
        create_credit_user_request: CreateCreditUserRequest,
) -> CreditRequestRequest:
    account_response = api_manager.user_steps.create_account(
        create_credit_user_request
    )

    return CreditRequestRequest(
        accountId=account_response.id,
        amount=CreditRule.get_contract_valid_but_rejected_amount(),
        termMonths=CreditRule.generate_valid_term_months(),
    )
