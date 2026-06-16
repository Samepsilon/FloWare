import csv
import os
from app.Models.notifica import Notifica
BASE_DIR = os.path.abspath("..")
FILE = BASE_DIR + "/Data/notifiche.csv"

COLONNE = ["id", "destinatario", "messaggio", "letta", "tipo", "richiestaId"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        righe = []
        for r in csv.DictReader(f):
            righe.append(Notifica(
                id=int(r["id"]),
                destinatario=r["destinatario"],
                messaggio=r["messaggio"],
                letta=r["letta"] == "True",
                tipo=r["tipo"],
                richiestaId=int(r["richiestaId"]) if r["richiestaId"] else None,
            ))
        return righe


def scrivi(notifiche):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNE)
        w.writeheader()
        for n in notifiche:
            w.writerow({
                "id": n.id,
                "destinatario": n.destinatario,
                "messaggio": n.messaggio,
                "letta": n.letta,
                "tipo": n.tipo,
                "richiestaId": n.richiestaId if n.richiestaId is not None else "",
            })


def salvaNotifica(notifica):
    tutti = leggi()
    if notifica.id is None:
        notifica.id = max((n.id for n in tutti), default=0) + 1
        tutti.append(notifica)
    else:
        tutti = [notifica if n.id == notifica.id else n for n in tutti]
    scrivi(tutti)
    return notifica


def segnaComeLetta(idNotifica):
    notifica = trovaNotifica(idNotifica)
    if notifica:
        notifica.letta = True
        salvaNotifica(notifica)
        return True
    return False


def creaNotifica(cliente, stato):
    destinatario = cliente.username if hasattr(cliente, "username") else str(cliente)
    notifica = Notifica(
        destinatario=destinatario,
        messaggio=f"Stato aggiornato: {stato}",
        letta=False,
        tipo="stato",
    )
    return salvaNotifica(notifica)


def inviaNotifica(destinatario, messaggio):
    notifica = Notifica(
        destinatario=destinatario,
        messaggio=messaggio,
        letta=False,
        tipo="generica",
    )
    return salvaNotifica(notifica)


def trovaNotifica(id):
    for n in leggi():
        if n.id == id:
            return n
    return None


def notificheNonLette():
    return [n for n in leggi() if not n.letta]


def notificheDelDestinatario(destinatario):
    return [n for n in leggi() if n.destinatario == destinatario]


def notifichePerTipo(tipo):
    return [n for n in leggi() if n.tipo == tipo]


def notifichePerRichiesta(richiestaId):
    return [n for n in leggi() if n.richiestaId == richiestaId]


def eliminaNotifica(id):
    scrivi([n for n in leggi() if n.id != id])
