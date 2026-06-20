import csv
import os
from app.Models.notifica import Notifica

class NotificaRepository:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE = os.path.join(BASE_DIR, "Data", "notifiche.csv")
    COLONNE = ["id", "destinatario", "messaggio", "letta", "tipo", "richiestaId"]

    @classmethod
    def leggi(cls):
        if not os.path.exists(cls.FILE):
            return []
        with open(cls.FILE, newline="", encoding="utf-8") as f:
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

    @classmethod
    def scrivi(cls, notifiche):
        os.makedirs(os.path.dirname(cls.FILE), exist_ok=True)
        with open(cls.FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cls.COLONNE)
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

    @classmethod
    def salvaNotifica(cls, notifica):
        tutti = cls.leggi()
        if notifica.id is None:
            notifica.id = max((n.id for n in tutti), default=0) + 1
            tutti.append(notifica)
        else:
            tutti = [notifica if n.id == notifica.id else n for n in tutti]
        cls.scrivi(tutti)
        return notifica

    @classmethod
    def segnaComeLetta(cls, idNotifica):
        notifica = cls.trovaNotifica(idNotifica)
        if notifica:
            notifica.letta = True
            cls.salvaNotifica(notifica)
            return True
        return False

    @classmethod
    def creaNotifica(cls, cliente, stato):
        destinatario = cliente.username if hasattr(cliente, "username") else str(cliente)
        notifica = Notifica(
            destinatario=destinatario,
            messaggio=f"Stato aggiornato: {stato}",
            letta=False,
            tipo="stato",
        )
        return cls.salvaNotifica(notifica)

    @classmethod
    def inviaNotifica(cls, destinatario, messaggio):
        notifica = Notifica(
            destinatario=destinatario,
            messaggio=messaggio,
            letta=False,
            tipo="generica",
        )
        return cls.salvaNotifica(notifica)

    @classmethod
    def trovaNotifica(cls, id):
        for n in cls.leggi():
            if n.id == id:
                return n
        return None

    @classmethod
    def notificheNonLette(cls):
        return [n for n in cls.leggi() if not n.letta]

    @classmethod
    def notificheDelDestinatario(cls, destinatario):
        return [n for n in cls.leggi() if n.destinatario == destinatario]

    @classmethod
    def notifichePerTipo(cls, tipo):
        return [n for n in cls.leggi() if n.tipo == tipo]

    @classmethod
    def notifichePerRichiesta(cls, richiestaId):
        return [n for n in cls.leggi() if n.richiestaId == richiestaId]

    @classmethod
    def eliminaNotifica(cls, id):
        cls.scrivi([n for n in cls.leggi() if n.id != id])
