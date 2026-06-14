import re
from app.Repos import utenteRepository as repo

mail_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

_sessione = {"utente": None, "ruolo": None}


def inviaCredenziali(username, password):
    utente = repo.trovaPerCredenziali(username, password)
    if utente is None:
        raise ValueError("Credenziali non valide.")
    impostaSessione(utente.getRuolo())
    _sessione["utente"] = utente
    return utente


def impostaSessione(ruolo):
    _sessione["ruolo"] = ruolo


def reindirizzaPerRuolo(ruolo):
    if ruolo == "cliente":
        return "InterfacciaCliente"
    if ruolo == "negoziante":
        return "InterfacciaNegoziante"
    raise ValueError(f"Ruolo non riconosciuto: {ruolo}")


def getSessione():
    return _sessione.copy()


def verificaFormatoEmail(email):
    return bool(re.match(mail_pattern, email))


def confrontaPassword(password, conferma):
    return password == conferma
