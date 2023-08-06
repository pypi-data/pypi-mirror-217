from typing import Optional


class AuthUser:
    def __init__(self) -> None:
        self.username: Optional[str] = None
        self.email: Optional[str] = None
        self.matricula: Optional[str] = None
        self.cpf: Optional[str] = None
        self.ativo: Optional[bool] = None
        self.nome: Optional[str] = None
        self.tipo_usuario: Optional[str] = None

    def from_json(self, dados: dict):
        self.username = dados["username"]
        self.email = dados["email"]
        self.matricula = dados["matricula"]
        self.cpf = dados["cpf"]
        self.ativo = dados["ativo"]
        self.nome = dados["nome"]
        self.tipo_usuario = dados["tipo_usuario"]
