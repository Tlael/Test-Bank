import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest


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
        amount=1000
    )

    api_manager.user_steps.deposit_account(
        create_user_request,
        deposit_request
    )

    return first_account, second_account