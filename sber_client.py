import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class SberClient:

    def __init__(self, base_url, client_id, client_secret, cert, key, ca="/app/sber_ca.pem"):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret

        timeout = httpx.Timeout(connect=10.0, read=30.0, write=30.0, pool=30.0)
        limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)

        self.client = httpx.Client(
            base_url=self.base_url,
            cert=(cert, key),
            verify=ca,
            timeout=timeout,
            limits=limits,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            http2=True
        )

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        retry=retry_if_exception_type(httpx.HTTPError)
    )
    def get_token(self):
        r = self.client.post(
            "/ic/sso/api/v2/oauth/token",
            auth=(self.client_id, self.client_secret),
            json={
                "grant_type": "client_credentials",
                "scope": "openid"
            }
        )
        r.raise_for_status()
        return r.json()["access_token"]

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        retry=retry_if_exception_type(httpx.HTTPError)
    )
    def get_balance(self, token, account):
        r = self.client.get(
            f"/v1/accounts/{account}/balance",
            headers={"Authorization": f"Bearer {token}"}
        )
        r.raise_for_status()
        return float(r.json()["balance"])

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        retry=retry_if_exception_type(httpx.HTTPError)
    )
    def get_interest_rate(self, token, amount):
        r = self.client.get(
            "/v1/placement/interest-rate",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "product": "OVERNIGHT",
                "amount": amount,
                "term": 1
            }
        )
        r.raise_for_status()
        return r.json()["interestRate"]

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        retry=retry_if_exception_type(httpx.HTTPError)
    )
    def create_deposit(self, token, amount, rate, external_id):
        payload = {
            "externalId": external_id,
            "product": "OVERNIGHT",
            "term": 1,
            "amount": amount,
            "interestRate": rate
        }

        r = self.client.post(
            "/v2/placement/deposit/application/interest-rate",
            headers={"Authorization": f"Bearer {token}"},
            json=payload
        )

        r.raise_for_status()
        return r.json()

    def get_application_state(self, token, external_id):
        r = self.client.get(
            f"/v1/placement/deposit/application/{external_id}/state",
            headers={"Authorization": f"Bearer {token}"}
        )
        r.raise_for_status()
        return r.json()

    def get_application(self, token, external_id):
        r = self.client.get(
            f"/v1/placement/deposit/application/{external_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        r.raise_for_status()
        return r.json()
