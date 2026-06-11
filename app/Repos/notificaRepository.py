import csv
import os
from app.Models.notifica import Notifica

FILE = "data/notifiche.csv"
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


def salva_notifica(notifica):
    tutti = leggi()
    if notifica.id is None:
        notifica.id = max((n.id for n in tutti), default=0) + 1
        tutti.append(notifica)
    else:
        tutti = [notifica if n.id == notifica.id else n for n in tutti]
    scrivi(tutti)
    return notifica


def trova_notifica(id):
    for n in leggi():
        if n.id == id:
            return n
    return None


def trovaPerId(id):
    return trova_notifica(id)


def notifiche_del_destinatario(destinatario):
    return [n for n in leggi() if n.destinatario == destinatario]


def notifiche_non_lette():
    return [n for n in leggi() if not n.letta]


def notifiche_per_tipo(tipo):
    return [n for n in leggi() if n.tipo == tipo]


def notifiche_per_richiesta(richiestaId):
    return [n for n in leggi() if n.richiestaId == richiestaId]


def elimina_notifica(id):
    tutti = leggi()
    filtrati = [n for n in tutti if n.id != id]
    scrivi(filtrati)


def elimina_notifiche_del_destinatario(destinatario):
    tutti = leggi()
    filtrati = [n for n in tutti if n.destinatario != destinatario]
    scrivi(filtrati)


def segna_come_letta(id):
    """Aggiorna lo stato 'letta' di una notifica"""
    notifica = trova_notifica(id)
    if notifica:
        notifica.letta = True
        salva_notifica(notifica)
        return True
    return False