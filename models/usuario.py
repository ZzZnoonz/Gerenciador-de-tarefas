# models/usuario.py
class Usuario:
    def __init__(self, nome: str, email: str):
        self._nome = nome
        self._email = email

    @property
    def nome(self):
        return self._nome