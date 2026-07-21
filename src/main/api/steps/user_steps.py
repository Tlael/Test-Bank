from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.crud_requester import CrudRequester
from main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from main.api.models.create_credit_user_request import CreateCreditUserRequest
from main.api.models.create_user_request import CreateUserRequest
from main.api.models.credit_repay_request import CreditRepayRequest
from main.api.models.credit_request_request import CreditRequestRequest
from main.api.models.deposit_account_request import DepositAccountRequest
from main.api.models.transfer_account_request import TransferAccountRequest
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs
from main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_create()
        ).post()
        return response

    def deposit_account(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(deposit_account_request)
        return response

    def deposit_invalid_account(self, create_user_request: CreateUserRequest,
                                deposit_account_request: DepositAccountRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(deposit_account_request)
        return response

    def transfer_account(self, create_user_request: CreateUserRequest, transfer_account_request: TransferAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(transfer_account_request)

        return response

    def transfer_invalid_account(self, create_user_request: CreateUserRequest, transfer_account_request: TransferAccountRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(transfer_account_request)

        return response

    def credit_request(self, credit_user_request: CreateCreditUserRequest, credit_request_model: CreditRequestRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=credit_user_request.username, password=credit_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_create()
        ).post(credit_request_model)

        return response

    def credit_invalid_request(self, credit_user_request: CreateCreditUserRequest, credit_request_model: CreditRequestRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=credit_user_request.username, password=credit_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_bad()
        ).post(credit_request_model)

        return response

    def credit_repay_request(self, credit_user_request: CreateCreditUserRequest, credit_repay_request_model: CreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=credit_user_request.username, password=credit_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request_model)
        return response

    def credit_invalid_repay(self, credit_user_request: CreateCreditUserRequest, credit_repay_request_model: CreditRepayRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=credit_user_request.username, password=credit_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.unprocessable_entity()
        ).post(credit_repay_request_model)
        return response