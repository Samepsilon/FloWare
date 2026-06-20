"""
Questo modulo gestisce l'invio e la visualizzazione delle notifiche destinate ai clienti
e ai negozianti, incluse le conferme delle richieste (appuntamenti, preventivi, ecc.).
"""

from app.Models.notifica import Notifica
from app.Repos.notificaRepository import NotificaRepository
from app.Repos.archivioRichieste import ArchivioRichieste
from app.Repos.consegnaRepository import ConsegnaRepository

class GestoreNotifiche:
    @classmethod
    def visualizzaNotifiche(cls):
        return NotificaRepository.notificheNonLette()

    @classmethod
    def confermaRichiesta(cls, richiesta, tipo_atteso):
        if isinstance(richiesta, int):
            richiesta = ArchivioRichieste.trovaPerId(richiesta)
        if richiesta is None:
            raise ValueError("Richiesta non trovata.")
        if richiesta.tipo != tipo_atteso:
            raise ValueError(f"La richiesta non è di tipo {tipo_atteso}.")
        richiesta = ArchivioRichieste.aggiornaStatoRichiesta(richiesta, "confermata")
        notifica = Notifica(
            destinatario=str(richiesta.clienteId),
            messaggio=f"Richiesta {richiesta.tipo} confermata.",
            letta=False,
            tipo="conferma",
            richiestaId=richiesta.id,
        )
        return cls.inviaNotificaCliente(notifica.destinatario, notifica.messaggio)

    @classmethod
    def confermaAppuntamento(cls, richiesta):
        return cls.confermaRichiesta(richiesta, "appuntamento")

    @classmethod
    def confermaPreventivo(cls, richiesta):
        return cls.confermaRichiesta(richiesta, "preventivo")

    @classmethod
    def inviaNotificaCliente(cls, destinatario, messaggio):
        return NotificaRepository.inviaNotifica(destinatario, messaggio)

    @classmethod
    def visualizzaConsegne(cls):
        return ConsegnaRepository.cercaConsegne()
