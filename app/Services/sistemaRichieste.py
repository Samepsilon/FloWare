from app.Models.richiesta import Richiesta, TIPI_VALIDI
from app.Models.notifica import Notifica
from app.Repos.archivioRichieste import ArchivioRichieste
from app.Repos.notificaRepository import NotificaRepository
from app.Repos.utenteRepository import UtenteRepository
from app.Repos.archivioCalendario import ArchivioCalendario

class SistemaRichieste:
    @classmethod
    def richiediOpzioni(cls):
        return list(TIPI_VALIDI)

    @classmethod
    def inviaRichiesta(cls, richiesta):
        if isinstance(richiesta, dict):
            richiesta = Richiesta(**richiesta)
        if richiesta.tipo not in TIPI_VALIDI:
            raise ValueError(f"Tipo non valido. Scegli tra: {TIPI_VALIDI}")
        if not richiesta.descrizione or not richiesta.descrizione.strip():
            raise ValueError("La descrizione non può essere vuota.")
        if not richiesta.contatti or not richiesta.contatti.strip():
            raise ValueError("I contatti non possono essere vuoti.")
        if UtenteRepository.trovaPerId(richiesta.clienteId) is None:
            raise ValueError(f"Cliente con id={richiesta.clienteId} non trovato.")

        richiesta = ArchivioRichieste.salva(richiesta)
        notifica = Notifica(
            destinatario="negoziante",
            messaggio=f"Nuova richiesta {richiesta.tipo} da cliente id={richiesta.clienteId}",
            letta=False,
            tipo=richiesta.tipo,
            richiestaId=richiesta.id,
        )
        NotificaRepository.salvaNotifica(notifica)
        return richiesta

    @classmethod
    def annullaRichiesta(cls, idRichiesta):
        richiesta = ArchivioRichieste.trovaPerId(idRichiesta)
        if richiesta is None:
            raise ValueError(f"Richiesta con id={idRichiesta} non trovata.")
        if not ArchivioRichieste.verificaAnnullamento(richiesta):
            raise ValueError("La richiesta non è più annullabile.")
        return ArchivioRichieste.aggiornaStatoRichiesta(richiesta, "annullata")

    @classmethod
    def recuperaRichieste(cls, clienteId):
        return ArchivioRichieste.trovaPerCliente(clienteId)

    @classmethod
    def getDettagliRichiesta(cls, idRichiesta):
        return ArchivioRichieste.trovaPerId(idRichiesta)

    @classmethod
    def recuperaDateDisponibili(cls):
        return ArchivioCalendario.trovaDateLibere()

    @classmethod
    def recuperaFasceOrarie(cls, data):
        return ArchivioCalendario.trovaFascePerData(data)

    @classmethod
    def confermaScelta(cls, data, ora):
        return ArchivioCalendario.salvaScelta(data, ora)
