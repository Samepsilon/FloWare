"""
Questo modulo gestisce il sistema di registrazione dei nuovi utenti del negozio,
validando i requisiti di email e password e salvando i dati degli utenti.
"""

import re
from app.Models.negoziante import Negoziante
from app.Models.cliente import Cliente
from app.Repos.utenteRepository import UtenteRepository

class SistemaRegistrazione:
    mail_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{6,20}$"

    @classmethod
    def inviaRegistrazione(cls, dati):
        username = dati["username"]
        email = dati["email"]
        password = dati["password"]
        ruolo = dati.get("ruolo", "cliente")

        if UtenteRepository.trovaPerUsername(username):
            raise ValueError(f"Username '{username}' già in uso.")
        if not cls.verificaFormatoEmail(email):
            raise ValueError("Formato email non valido.")
        if not cls.verificaCriteriPassword(password):
            raise ValueError("La password non rispetta i criteri richiesti.")

        if ruolo == "negoziante":
            utente = Negoziante(username, email, password)
        else:
            utente = Cliente(username, email, password)
        return UtenteRepository.salva(utente)

    @classmethod
    def verificaFormatoEmail(cls, email):
        return bool(re.match(cls.mail_pattern, email))

    @classmethod
    def verificaCriteriPassword(cls, password):
        return bool(re.search(cls.password_pattern, password))

    @classmethod
    def confrontaPassword(cls, password, conferma):
        return password == conferma