import csv
import os
from app.Models.richiesta import Richiesta
from app.Models.notifica import Notifica
from app.Repos import notificaRepository as repoNotifiche
BASE_DIR = os.path.abspath("..")
FILE = BASE_DIR + "/Data/richieste.csv"

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
                data=r["data"],
                ora=r["ora"],
                contatti=r["contatti"],
                descrizione=r["descrizione"],
                clienteId=int(r["clienteId"]) if r["clienteId"] else None,
            ))
        return righe


def scrivi(richieste):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNE)
        w.writeheader()
        for r in richieste:
            w.writerow({
                "id": r.id,
                "tipo": r.tipo,
                "stato": r.stato,
                "data": r.data,
                "ora": r.ora,
                "contatti": r.contatti,
                "descrizione": r.descrizione,
                "clienteId": r.clienteId if r.clienteId is not None else "",
            })


def salva(richiesta):
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


def getDettagliConferma(id):
    r = trovaPerId(id)
    if r is None or r.stato != "confermata":
        return None
    return r


def findNotificheNonLette():
    return repoNotifiche.notificheNonLette()


def verificaAnnullamento(richiesta):
    return richiesta is not None and richiesta.stato == "in attesa"


def cercaRichiesta(richiesta):
    for r in leggi():
        if r.id == richiesta.id:
            return r
    return None


def aggiornaStatoRichiesta(richiesta, stato):
    if richiesta is None:
        return None
    richiesta.setStato(stato)
    return salva(richiesta)


def richiesteInAttesa():
    return [r for r in leggi() if r.stato == "in attesa"]

def eliminaRichiesta(id):
    scrivi([r for r in leggi() if r.id != id])
