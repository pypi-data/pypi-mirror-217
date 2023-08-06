import requests
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http.request import HttpRequest

from .access_token_response import AccessTokenResponse
from .auth_user import AuthUser


class SSOAuth:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        response_type: str,
        sso_url: str,
        callback_redirect_url: str,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.response_type = response_type
        self.sso_url = sso_url
        self.callback_redirect_url = callback_redirect_url

    def url_de_autorizacao(self) -> str:
        endpoint = "{}/oauth/authorize".format(self.sso_url)
        return "{}?client_id={}&redirect_uri={}&response_type=code".format(
            endpoint,
            self.client_id,
            self.callback_redirect_url,
        )

    def obter_access_token(
        self,
        request: HttpRequest,
        token_de_permissao,
    ) -> bool:
        endpoint = "{}/oauth/token".format(self.sso_url)
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": token_de_permissao,
            "grant_type": "authorization_code",
            "redirect_uri": self.callback_redirect_url,
        }
        response = requests.post(endpoint, data=payload)

        if response.status_code >= 200 and response.status_code < 300:
            dados_de_acesso = AccessTokenResponse()
            dados_de_acesso.from_json(dicionario=response.json())
            access_token = dados_de_acesso.access_token
            dados_usuario = self.dados_usuario_logado(token=access_token)
            self.salvar_sessao(request, dados_de_acesso)
            self.autenticar_usuario(request=request, dados=dados_usuario)
            return True
        return False

    def salvar_sessao(self, request, dados):
        request.session.clear()
        request.session["access_token"] = dados.access_token
        request.session["validade"] = dados.expires_in

    def autenticar_usuario(self, request, dados: AuthUser):
        resultado_busca = User.objects.filter(username=dados.username)

        if resultado_busca.exists():
            usuario = resultado_busca.first()
            login(
                request=request,
                user=usuario,
                backend="django.contrib.auth.backends.ModelBackend",
            )
        else:
            usuario = User.objects.create_user(
                username=dados.username,
                email=dados.email,
            )
            login(
                request=request,
                user=usuario,
                backend="django.contrib.auth.backends.ModelBackend",
            )

    def dados_usuario_logado(self, token) -> AuthUser:
        endpoint = "{}/api/v1/me".format(self.sso_url)
        headers = {"Authorization": "Bearer {}".format(token)}
        response = requests.get(endpoint, headers=headers)
        if response.status_code >= 200 and response.status_code < 300:
            instancia_usuario = AuthUser()
            instancia_usuario.from_json(dados=response.json())
            return instancia_usuario

    def logout(self, request: HttpRequest) -> str:
        return "{}/logout".format(self.sso_url)
