import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class SberClient:

    def __init__(self, base_url, client_id, client_secret, cert, key):

        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret

        self.client = httpx.Client(
            base_url=base_url,
            cert=("/app/sandbox_cert.pem", "/app/sandbox_key.pem"),
            timeout=30.0
        )

    @retry(stop=stop_after_attempt(5), wait=wait_exponential())
    def get_token(self):

        r = self.client.post(
            f"{self.base_url}/ic/sso/api/v2/oauth/token",
            auth=(self.client_id, self.client_secret),
            json={
                "grant_type": "client_credentials",
                "scope": "openid"
            }
        )

        r.raise_for_status()

        return r.json()["access_token"]

    @retry(stop=stop_after_attempt(5), wait=wait_exponential())
    def get_balance(self, token, account):

        r = self.client.get(
            f"{self.base_url}/v1/accounts/{account}/balance",
            headers={"Authorization": f"Bearer {token}"}
        )

        r.raise_for_status()

        return float(r.json()["balance"])

    @retry(stop=stop_after_attempt(5), wait=wait_exponential())
    def get_interest_rate(self, token, amount):

        r = self.client.get(
            f"{self.base_url}/v1/placement/interest-rate",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "product": "OVERNIGHT",
                "amount": amount,
                "term": 1
            }
        )

        r.raise_for_status()

        return r.json()["interestRate"]

    @retry(stop=stop_after_attempt(5), wait=wait_exponential())
    def create_deposit(self, token, amount, rate, external_id):

        payload = {
            "externalId": external_id,
            "product": "OVERNIGHT",
            "term": 1,
            "amount": amount,
            "interestRate": rate
        }

        r = self.client.post(
            f"{self.base_url}/v2/placement/deposit/application/interest-rate",
            headers={"Authorization": f"Bearer {token}"},
            json=payload
        )

        r.raise_for_status()

        return r.json()

    def get_application_state(self, token, external_id):

        r = self.client.get(
            f"{self.base_url}/v1/placement/deposit/application/{external_id}/state",
            headers={"Authorization": f"Bearer {token}"}
        )

        r.raise_for_status()

        return r.json()

    def get_application(self, token, external_id):

        r = self.client.get(
            f"{self.base_url}/v1/placement/deposit/application/{external_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        r.raise_for_status()

        return r.json()
