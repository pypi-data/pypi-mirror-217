import requests
from typing import Dict


class Facteur:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError('API key is required')
        self.api_key = api_key

    def __get_headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }

    def __call_api(self, path: str, params: Dict = None):
        if not params:
            params = {}

        response = requests.post(
            "https://facteur.dev" + path,
            headers=self.__get_headers(),
            json=params,
        )

        if response.status_code != 200:
            raise Exception(response.json()["error"])

        return response.json()

    def send_email(self,
                   frm: str,
                   to: str,
                   subject: str,
                   html: str = None,
                   text: str = None):
        path = "/api/v1/emails"
        params = {
            "from": frm,
            "to": to,
            "subject": subject,
            "html": html,
            "text": text,
        }

        self.__call_api(path, params)
