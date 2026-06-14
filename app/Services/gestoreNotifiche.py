from app.Models.notifica import Notifica
from app.Repos import notificaRepository as repoN
from app.Repos import archivioRichieste as repoR
from app.Repos import consegnaRepository as repoC


def visualizzaNotifiche():
    return repoN.notificheNonLette()


def confermaAppuntamento(richiesta):
    return _confermaRichiesta(richiesta, "appuntamento")


def confermaPreventivo(richiesta):
    return _confermaRichiesta(richiesta, "preventivo")


def _confermaRichiesta(richiesta, tipo_atteso):
    if isinstance(richiesta, int):
        richiesta = repoR.trovaPerId(richiesta)
    if richiesta is None:
        raise ValueError("Richiesta non trovata.")
    if richiesta.tipo != tipo_atteso:
        raise ValueError(f"La richiesta non è di tipo {tipo_atteso}.")
    richiesta = repoR.aggiornaStatoRichiesta(richiesta, "confermata")
    notifica = Notifica(
        destinatario=str(richiesta.clienteId),
        messaggio=f"Richiesta {richiesta.tipo} confermata.",
        letta=False,
        tipo="conferma",
        richiestaId=richiesta.id,
    )
    return inviaNotificaCliente(notifica)


def inviaNotificaCliente(notifica):
    return repoN.salvaNotifica(notifica)


def visualizzaConsegne():
    return repoC.cercaConsegne()
