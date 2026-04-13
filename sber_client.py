import httpx


class SberClient:

    def __init__(self, base_url, client_id, client_secret, cert, key):

        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret

        self.client = httpx.Client(
            cert=(cert, key),
            timeout=30
        )

    def get_token(self):

        url = f"{self.base_url}/ic/sso/api/v2/oauth/token"

        response = self.client.post(
            url,
            auth=(self.client_id, self.client_secret),
            json={
                "grant_type": "client_credentials",
                "scope": "openid"
            }
        )

        response.raise_for_status()

        return response.json()["access_token"]

    def get_balance(self, token, account):

        url = f"{self.base_url}/v1/accounts/{account}/balance"

        response = self.client.get(
            url,
            headers={"Authorization": f"Bearer {token}"}
        )

        response.raise_for_status()

        data = response.json()

        return float(data["balance"])

    def get_interest_rate(self, token, amount):

        url = f"{self.base_url}/v1/placement/interest-rate"

        response = self.client.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params={
                "product": "OVERNIGHT",
                "amount": amount,
                "term": 1
            }
        )

        response.raise_for_status()

        return response.json()["interestRate"]

    def create_deposit(self, token, amount, rate, external_id):

        url = f"{self.base_url}/v2/placement/deposit/application/interest-rate"

        payload = {
            "externalId": external_id,
            "product": "OVERNIGHT",
            "term": 1,
            "amount": amount,
            "interestRate": rate
        }

        response = self.client.post(
            url,
            headers={"Authorization": f"Bearer {token}"},
            json=payload
        )

        response.raise_for_status()

        return response.json()

    def get_application_state(self, token, external_id):

        url = f"{self.base_url}/v1/placement/deposit/application/{external_id}/state"

        response = self.client.get(
            url,
            headers={"Authorization": f"Bearer {token}"}
        )

        response.raise_for_status()

        return response.json()
