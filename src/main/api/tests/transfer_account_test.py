import requests
import pytest


@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(self):
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

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Vika113",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"}
        )

        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Vika113",
                "password": "Pas!sw0rd",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response.status_code == 201
        account_id = create_account_response.json().get("id")

        deposit_account_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": account_id,
                "amount": 1000
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        assert deposit_account_response.status_code == 200

        transfer_account_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": account_id,
                  "toAccountId": 2,
                  "amount": 500.75
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        assert transfer_account_response.status_code == 200
        assert transfer_account_response.json().get("fromAccountId") == account_id
        assert transfer_account_response.json().get("toAccountId") == 2

    def test_transfer_account_invalid(self):
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

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Vika114",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"}
        )

        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Vika114",
                "password": "Pas!sw0rd",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response.status_code == 201
        account_id = create_account_response.json().get("id")

        deposit_account_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": account_id,
                "amount": 1000
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        assert deposit_account_response.status_code == 200


        transfer_account_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": account_id,
                  "toAccountId": 2,
                  "amount": 499
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        assert transfer_account_response.status_code == 400
        assert transfer_account_response.json().get("error") == "Amount must be between 500 and 10000"
