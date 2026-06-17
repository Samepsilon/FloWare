from app.Models.consegna import Consegna
from app.Models.notifica import Notifica
from app.Repos.consegnaRepository import ConsegnaRepository
from app.Repos.notificaRepository import NotificaRepository
from app.Repos.utenteRepository import UtenteRepository

class GestoreConsegne:
    @classmethod
    def confermaRichiesta(cls, dati):
        cliente_id = dati.get("clienteId")
        if UtenteRepository.trovaPerId(cliente_id) is None:
            raise ValueError(f"Cliente con id={cliente_id} non trovato.")

        consegna = Consegna(
            regione=dati["regione"],
            citta=dati.get("citta", dati.get("città", "")),
            via=dati["via"],
            civico=dati["civico"],
            stato="in attesa",
            clienteId=cliente_id,
        )
        consegna = ConsegnaRepository.salva(consegna)

        notifica = Notifica(
            destinatario="negoziante",
            messaggio=f"Nuova richiesta consegna da cliente id={cliente_id}",
            letta=False,
            tipo="consegna",
        )
        NotificaRepository.salvaNotifica(notifica)
        return consegna

    @classmethod
    def trovaPerId(cls, idConsegna):
        return ConsegnaRepository.trovaPerId(idConsegna)

    @classmethod
    def aggiornaStatoConsegna(cls, idConsegna, nuovoStato):
        consegna = ConsegnaRepository.trovaPerId(idConsegna)
        if consegna is None:
            raise ValueError(f"Consegna con id={idConsegna} non trovata.")
        consegna.setStato(nuovoStato)
        consegna = ConsegnaRepository.salva(consegna)

        cliente = UtenteRepository.trovaPerId(consegna.getClienteId())
        if cliente:
            NotificaRepository.creaNotifica(cliente, nuovoStato)
        return consegna

    @classmethod
    def cercaConsegne(cls):
        return ConsegnaRepository.cercaConsegne()
