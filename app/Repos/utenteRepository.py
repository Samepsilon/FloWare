import csv
import os
from app.Models.cliente import Cliente
from app.Models.negoziante import Negoziante

FILE = "data/utenti.csv"
COLONNE = ["id", "ruolo", "username", "email", "password"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        utenti = []
        for r in csv.DictReader(f):
            if r["ruolo"] == "cliente":
                utenti.append(Cliente(
                    id=int(r["id"]),
                    username=r["username"],
                    email=r["email"],
                    password=r["password"],
                ))
            else:
                utenti.append(Negoziante(
                    id=int(r["id"]),
                    username=r["username"],
                    email=r["email"],
                    password=r["password"],
                ))
        return utenti


def scrivi(utenti):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNE)
        w.writeheader()
        for u in utenti:
            w.writerow({
                "id": u.id,
                "ruolo": u.ruolo,
                "username": u.username,
                "email": u.email,
                "password": u.password,
            })


def salva(nuovoCliente):
    tutti = leggi()
    if nuovoCliente.id is None:
        nuovoCliente.id = max((u.id for u in tutti), default=0) + 1
        tutti.append(nuovoCliente)
    else:
        tutti = [nuovoCliente if u.id == nuovoCliente.id else u for u in tutti]
    scrivi(tutti)
    return nuovoCliente


def trovaPerCredenziali(username, password):
    for u in leggi():
        if u.username == username and u.password == password:
            return u
    return None


def trovaPerId(id):
    for u in leggi():
        if u.id == id:
            return u
    return None


def trovaPerUsername(username):
    for u in leggi():
        if u.username == username:
            return u
    return None


def trovaPerEmail(email):
    for u in leggi():
        if u.email == email:
            return u
    return None


def tuttiClienti():
    return [u for u in leggi() if u.ruolo == "cliente"]


def tuttiNegozianti():
    return [u for u in leggi() if u.ruolo == "negoziante"]


def eliminaUtente(id):
    tutti = leggi()
    scrivi([u for u in tutti if u.id != id])
