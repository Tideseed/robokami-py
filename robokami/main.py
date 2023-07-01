import requests
import os
import sseclient
from datetime import datetime


class RKClient:
    def __init__(self, creds, server="https://idm.robokami.com", **kwargs) -> None:
        self.server = server
        self.creds = creds
        if kwargs.get("initiate_login", True):
            self.authorize()

        if kwargs.get("initiate_stream", False) and self.session_token is not None:
            self.stream()

    def authorize(self):
        res = requests.get(
            os.path.join(self.server, "login"),
            json={"credentials": self.creds},
            timeout=15,
        )

        if res.status_code == 200:
            self.session_token = res.json()["session_token"]
            self.iat = datetime.now().timestamp()
        else:
            print("Login failed")
            self.session_token = None

    def renew_session(self):
        self.authorize()

    def place_order(self, d):
        d["status"] = d.get("status", "active")
        d["explanation"] = d.get("explanation", "RK-TRADER")
        return self.trade_command("place_order", d)

    def update_order(self, d):
        if "order_id" not in d.keys():
            return {"status": "error", "message": "order_id is required"}
        d["contract_type"] = "hourly" if d["contract"].startswith("PH") else "block"
        d["explanation"] = d.get("explanation", "RK-TRADER")
        return self.trade_command("update_order", d)

    def trade_command(self, command, d):
        res = requests.post(
            os.path.join(self.server, "trade", command),
            headers={"Authorization": self.session_token},
            json=d,
        )

        if res.status_code == 200:
            return res.json()
        else:
            print("Failed response code: " + str(res.status_code))
            print(res.json())
            return res.json()

    def stream(self):
        response = requests.get(
            os.path.join(self.server, "stream"),
            headers={"Authorization": self.session_token},
            stream=True,
        )

        self.stream_client = sseclient.SSEClient(response)
