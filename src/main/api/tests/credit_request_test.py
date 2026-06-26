import requests
import pytest


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_valid(self):
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
                "username": "Vika126",
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
                "username": "Vika126",
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
        assert credit_request_response.json().get("amount") == 5000
        assert credit_request_response.json().get("termMonths") == 12

    def test_credit_request_invalid(self):
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
                "username": "Vika134",
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
                "username": "Vika134",
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
            json={"accountId": 1,
                  "amount": 20000,
                  "termMonths": 12
                  },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert credit_request_response.status_code == 400
        assert credit_request_response.json().get("error") == "Amount must be between 5000 and 15000"