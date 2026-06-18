import csv
import os
from datetime import datetime
from app.Models.richiesta import Richiesta

FILE = "data/richieste.csv"
COLONNE = ["id", "tipo", "stato", "data", "ora", "contatti", "descrizione", "clienteId"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        righe = []
        for r in csv.DictReader(f):
            # Converte la data da stringa a oggetto date
            data_obj = datetime.strptime(r["data"], "%Y-%m-%d").date() if r["data"] else None
            
            righe.append(Richiesta(
                id=int(r["id"]),
                tipo=r["tipo"],
                stato=r["stato"],
                data=data_obj,
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
            # Converte la data da oggetto a stringa
            data_str = r.data.strftime("%Y-%m-%d") if r.data else ""
            
            w.writerow({
                "id": r.id,
                "tipo": r.tipo,
                "stato": r.stato,
                "data": data_str,
                "ora": r.ora,
                "contatti": r.contatti,
                "descrizione": r.descrizione,
                "clienteId": r.clienteId if r.clienteId is not None else "",
            })


def salva_richiesta(richiesta):
    tutte = leggi()
    if richiesta.id is None:
        richiesta.id = max((r.id for r in tutte), default=0) + 1
        tutte.append(richiesta)
    else:
        tutte = [richiesta if r.id == richiesta.id else r for r in tutte]
    scrivi(tutte)
    return richiesta


def trova_richiesta(id):
    for r in leggi():
        if r.id == id:
            return r
    return None


def trovaPerId(id):
    return trova_richiesta(id)


def richieste_per_cliente(clienteId):
    return [r for r in leggi() if r.clienteId == clienteId]


def richieste_per_tipo(tipo):
    return [r for r in leggi() if r.tipo == tipo]


def richieste_per_stato(stato):
    return [r for r in leggi() if r.stato == stato]


def richieste_in_attesa():
    return [r for r in leggi() if r.stato == "in_attesa"]


def richieste_completate():
    return [r for r in leggi() if r.stato == "completata"]


def richieste_per_data(data):
    return [r for r in leggi() if r.data == data]


def elimina_richiesta(id):
    tutte = leggi()
    filtrati = [r for r in tutte if r.id != id]
    scrivi(filtrati)


def elimina_richieste_del_cliente(clienteId):
    tutte = leggi()
    filtrati = [r for r in tutte if r.clienteId != clienteId]
    scrivi(filtrati)