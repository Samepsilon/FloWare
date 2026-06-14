import re
from app.Models.negoziante import Negoziante
from app.Models.cliente import Cliente
from app.Repos import utenteRepository as repo

mail_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{6,20}$"


def inviaRegistrazione(dati):
    username = dati["username"]
    email = dati["email"]
    password = dati["password"]
    ruolo = dati.get("ruolo", "cliente")

    if repo.trovaPerUsername(username):
        raise ValueError(f"Username '{username}' già in uso.")
    if not verificaFormatoEmail(email):
        raise ValueError("Formato email non valido.")
    if not verificaCriteriPassword(password):
        raise ValueError("La password non rispetta i criteri richiesti.")

    if ruolo == "negoziante":
        utente = Negoziante(username, email, password)
    else:
        utente = Cliente(username, email, password)
    return repo.salva(utente)


def verificaFormatoEmail(email):
    return bool(re.match(mail_pattern, email))


def verificaCriteriPassword(password):
    return bool(re.search(password_pattern, password))


def confrontaPassword(password, conferma):
    return password == conferma
