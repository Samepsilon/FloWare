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
                    ruolo=r["ruolo"],
                ))
            else:
                utenti.append(Negoziante(
                    id=int(r["id"]),
                    username=r["username"],
                    email=r["email"],
                    password=r["password"],
                    ruolo=r["ruolo"],
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


def salva_utente(utente):
    tutti = leggi()
    if utente.id is None:
        utente.id = max((u.id for u in tutti), default=0) + 1
        tutti.append(utente)
    else:
        tutti = [utente if u.id == utente.id else u for u in tutti]
    scrivi(tutti)
    return utente


def trova_utente(id):
    for u in leggi():
        if u.id == id:
            return u
    return None


def trova_per_username(username):
    for u in leggi():
        if u.username == username:
            return u
    return None


def trova_per_email(email):
    for u in leggi():
        if u.email == email:
            return u
    return None


def tutti_i_clienti():
    return [u for u in leggi() if u.ruolo == "cliente"]


def tutti_i_negozianti():
    return [u for u in leggi() if u.ruolo == "negoziante"]


def elimina_utente(id):
    tutti = leggi()
    filtrati = [u for u in tutti if u.id != id]
    scrivi(filtrati)




