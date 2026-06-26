import requests
import pytest


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_valid(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_credit_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Vika145",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"}
        )

        assert create_credit_user_response.status_code == 200

        login_credit_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Vika145",
                "password": "Pas!sw0rd",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        assert login_credit_user_response.status_code == 200
        token = login_credit_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response.status_code == 201
        account_id = create_account_response.json().get("id")

        credit_request_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={"accountId": account_id,
                  "amount": 5000,
                  "termMonths": 12
                  },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert credit_request_response.status_code == 201
        credit_id = credit_request_response.json().get("creditId")
        credit_amount = credit_request_response.json().get("amount")

        credit_repay_response = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json={
                "creditId": credit_id,
                "accountId": account_id,
                "amount": credit_amount
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert credit_repay_response.status_code == 200
        assert credit_repay_response.json().get("amountDeposited") == credit_amount
        assert credit_repay_response.json().get("creditId") == credit_id

    def test_credit_repay_invalid(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_credit_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Vika148",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"}
        )

        assert create_credit_user_response.status_code == 200

        login_credit_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Vika148",
                "password": "Pas!sw0rd",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        assert login_credit_user_response.status_code == 200
        token = login_credit_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response.status_code == 201
        account_id = create_account_response.json().get("id")

        credit_request_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={"accountId": account_id,
                  "amount": 5000,
                  "termMonths": 12
                  },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert credit_request_response.status_code == 201
        credit_id = credit_request_response.json().get("creditId")
        credit_amount = credit_request_response.json().get("amount")

        credit_repay_response = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json={
                "creditId": 999,
                "accountId": account_id,
                "amount": credit_amount
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert credit_repay_response.status_code == 404
        assert credit_repay_response.json().get(
            "error") == 'Credit with ID 999 was not found or does not belong to the user'
