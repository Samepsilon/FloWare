from app.Models.richiesta import Richiesta
from app.Models.slotOrario import slotOrario
from app.Models.notifica import Notifica

from app.Repos import richiestaRepository as repo
from app.Repos import notificaRepository as repoN
from app.Repos import utenteRepository as repoU

TIPI_VALIDI = ["preventivo", "appuntamento"]
STATI_VALIDI = ["in attesa", "confermata", "annullata"]


def invia_richiesta(cliente_id, tipo, descrizione, contatti, data="", ora=""):
    if tipo not in TIPI_VALIDI:
        raise ValueError(f"Tipo non valido. Scegli tra: {TIPI_VALIDI}")
    if not descrizione or not descrizione.strip():
        raise ValueError("La descrizione non può essere vuota.")
    if not contatti or not contatti.strip():
        raise ValueError("I contatti non possono essere vuoti.")
    if repoU.trova_utente(cliente_id) is None:
        raise ValueError(f"Cliente con id={cliente_id} non trovato.")

    r = Richiesta(tipo=tipo, descrizione=descrizione,contatti=contatti, data=data, ora=ora, clienteId=cliente_id)

    richiesta = repo.salva_richiesta(r)


    # notify the shop owner
    n = Notifica(
        destinatario="negoziante",
        messaggio=f"Nuova richiesta {tipo} da cliente id={cliente_id}: {descrizione[:60]}",
        tipo=tipo,
        richiestaId=richiesta.id,)
    repoN.salvaNotifica(n)
    return richiesta

def annulla_richiesta(richiesta_id, cliente_id):
    r = repo.trova_richiesta(richiesta_id)
    if r is None:
        raise ValueError(f"Richiesta con id={richiesta_id} non trovata.")
    if r.cliente_id != cliente_id:
        raise ValueError("Non puoi annullare una richiesta di un altro cliente.")
    if not repo.verificaAnnullamento(richiesta_id):
        raise ValueError("La richiesta non è più annullabile (non è in attesa).")
    return repo.aggiorna_stato_richiesta(richiesta_id, "annullata")

