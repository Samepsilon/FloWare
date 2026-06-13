import csv
import os
from app.Models.richiesta import Richiesta

TIPI_VALIDI = ["preventivo", "appuntamento"]
STATI_VALIDI = ["in attesa", "confermata", "annullata"]

FILE = "data/richiesta.csv"
COLONNE = ["id", "tipo", "stato", "data", "ora", "contatti", "descrizione", "clienteId"]

def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        righe = []
        for r in csv.DictReader(f):
            righe.append(Richiesta(
                id=int(r["id"]),
                tipo=r["tipo"],
                stato=r["stato"],
                data=(r["data"]),
                ora=r["ora"],
                contatti=(r["contatti"]),
                descrizione=(r["descrizione"]),
                clienteId=int(r["clienteId"]) if r["clienteId"] else None

            ))
        return righe

def scrivi(richiesta):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNE)
        w.writeheader()
        for a in richiesta:
            w.writerow({
                "id": a.id,
                "tipo": a.tipo,
                "stato": a.stato,
                "data": a.data,
                "ora": a.ora,
                "contatti": a.contatti,
                "descrizione": a.descrizione,
                "clienteId": a.clienteId if a.clienteId is not None else "",
            })

def salva_richiesta(richiesta):
    tutti = leggi()
    if richiesta.id is None:
        richiesta.id = max((r.id for r in tutti), default=0) + 1
        tutti.append(richiesta)
    else:
        tutti = [richiesta if r.id == richiesta.id else r for r in tutti]
    scrivi(tutti)
    return richiesta

def salva_richiesta(richiesta):
    tutti = leggi()
    if richiesta.id is None:
        richiesta.id = max((r.id for r in tutti), default=0) + 1
        tutti.append(richiesta)
    else:
        tutti = [richiesta if r.id == richiesta.id else r for r in tutti]
    scrivi(tutti)
    return richiesta


def trovaPerId(id):
    for r in leggi():
        if r.id == id:
            return r
    return None

def trovaPerCliente(clienteId):
    return [r for r in leggi() if r.clienteId == clienteId]

def aggiornaStatoRichiesta(id, nuovo_stato):
    r = trovaPerId(id)
    if r is None:
        return None
    r.stato = nuovo_stato
    salva_richiesta(r)
    return r


def verificaAnnullamento(richiesta):
    return richiesta is not None and richiesta.stato == "in attesa"

def richiesteInAttesa():
    return [r for r in leggi() if r.stato == "in_attesa"]


