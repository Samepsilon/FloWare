from app.Models.consegna import Consegna
from app.Models.notifica import Notifica
from app.Repos import consegnaRepository as repo
from app.Repos import notificaRepository as repoN
from app.Repos import utenteRepository as repoU


def confermaRichiesta(dati):
    cliente_id = dati.get("clienteId")
    if repoU.trovaPerId(cliente_id) is None:
        raise ValueError(f"Cliente con id={cliente_id} non trovato.")

    consegna = Consegna(
        regione=dati["regione"],
        citta=dati.get("citta", dati.get("città", "")),
        via=dati["via"],
        civico=dati["civico"],
        stato="in attesa",
        clienteId=cliente_id,
    )
    consegna = repo.salva(consegna)

    notifica = Notifica(
        destinatario="negoziante",
        messaggio=f"Nuova richiesta consegna da cliente id={cliente_id}",
        letta=False,
        tipo="consegna",
    )
    repoN.salvaNotifica(notifica)
    return consegna


def trovaPerId(idConsegna):
    return repo.trovaPerId(idConsegna)


def aggiornaStatoConsegna(idConsegna, nuovoStato):
    consegna = repo.trovaPerId(idConsegna)
    if consegna is None:
        raise ValueError(f"Consegna con id={idConsegna} non trovata.")
    consegna.setStato(nuovoStato)
    consegna = repo.salva(consegna)

    cliente = repoU.trovaPerId(consegna.getClienteId())
    if cliente:
        repoN.creaNotifica(cliente, nuovoStato)
    return consegna
