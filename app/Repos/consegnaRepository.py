import csv
import os
from app.Models.consegna import Consegna

FILE = "data/consegne.csv"
COLONNE = ["id", "regione", "citta", "via", "civico", "stato", "clienteId"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        righe = []
        for r in csv.DictReader(f):
            righe.append(Consegna(
                id=int(r["id"]),
                regione=r["regione"],
                citta=r.get("citta") or r.get("città", ""),
                via=r["via"],
                civico=r["civico"],
                stato=r["stato"] if r["stato"] else None,
                clienteId=int(r["clienteId"]) if r["clienteId"] else None,
            ))
        return righe


def scrivi(consegne):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNE)
        w.writeheader()
        for c in consegne:
            w.writerow({
                "id": c.id,
                "regione": c.regione,
                "citta": c.citta,
                "via": c.via,
                "civico": c.civico,
                "stato": c.stato if c.stato is not None else "",
                "clienteId": c.clienteId if c.clienteId is not None else "",
            })


def salva(consegna):
    tutti = leggi()
    if consegna.id is None:
        consegna.id = max((c.id for c in tutti), default=0) + 1
        tutti.append(consegna)
    else:
        tutti = [consegna if c.id == consegna.id else c for c in tutti]
    scrivi(tutti)
    return consegna


def trovaPerId(id):
    for c in leggi():
        if c.id == id:
            return c
    return None


def cercaConsegne():
    return leggi()

def consegneDelCliente(clienteId):
    return [c for c in leggi() if c.clienteId == clienteId]


def consegnePerStato(stato,clienteId):
    listConsegna = [c for c in leggi() if c.clienteId == clienteId]
    return [c for c in listConsegna if c.stato == stato]


def eliminaConsegna(id):
    scrivi([c for c in leggi() if c.id != id])
