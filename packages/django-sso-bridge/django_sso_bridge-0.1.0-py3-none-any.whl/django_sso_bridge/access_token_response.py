from typing import Optional


class AccessTokenResponse:
    def __init__(
        self,
        access_token: Optional[str] = None,
        token_type: Optional[str] = None,
        expires_in: Optional[int] = None,
        refresh_token: Optional[str] = None,
    ) -> None:
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.refresh_token = refresh_token

    def from_json(self, dicionario: dict) -> None:
        self.access_token = (dicionario["access_token"],)
        self.token_type = (dicionario["token_type"],)
        self.expires_in = (dicionario["expires_in"],)
        self.refresh_token = (dicionario["refresh_token"],)
