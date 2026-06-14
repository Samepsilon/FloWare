from app.Models.richiesta import Richiesta, TIPI_VALIDI
from app.Models.notifica import Notifica
from app.Repos import archivioRichieste as repo
from app.Repos import notificaRepository as repoN
from app.Repos import utenteRepository as repoU
from app.Repos import archivioCalendario as repoCalendario


def richiediOpzioni():
    return list(TIPI_VALIDI)


def inviaRichiesta(richiesta):
    if isinstance(richiesta, dict):
        richiesta = Richiesta(**richiesta)
    if richiesta.tipo not in TIPI_VALIDI:
        raise ValueError(f"Tipo non valido. Scegli tra: {TIPI_VALIDI}")
    if not richiesta.descrizione or not richiesta.descrizione.strip():
        raise ValueError("La descrizione non può essere vuota.")
    if not richiesta.contatti or not richiesta.contatti.strip():
        raise ValueError("I contatti non possono essere vuoti.")
    if repoU.trovaPerId(richiesta.clienteId) is None:
        raise ValueError(f"Cliente con id={richiesta.clienteId} non trovato.")

    richiesta = repo.salva(richiesta)
    notifica = Notifica(
        destinatario="negoziante",
        messaggio=f"Nuova richiesta {richiesta.tipo} da cliente id={richiesta.clienteId}",
        letta=False,
        tipo=richiesta.tipo,
        richiestaId=richiesta.id,
    )
    repoN.salvaNotifica(notifica)
    return richiesta


def annullaRichiesta(idRichiesta):
    richiesta = repo.trovaPerId(idRichiesta)
    if richiesta is None:
        raise ValueError(f"Richiesta con id={idRichiesta} non trovata.")
    if not repo.verificaAnnullamento(richiesta):
        raise ValueError("La richiesta non è più annullabile.")
    return repo.aggiornaStatoRichiesta(richiesta, "annullata")


def recuperaRichieste(clienteId):
    return repo.trovaPerCliente(clienteId)


def getDettagliRichiesta(idRichiesta):
    return repo.trovaPerId(idRichiesta)


def recuperaDateDisponibili():
    return repoCalendario.trovaDateLibere()


def recuperaFasceOrarie(data):
    return repoCalendario.trovaFascePerData(data)


def confermaScelta(data, ora):
    return repoCalendario.salvaScelta(data, ora)
