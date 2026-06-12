from app.Models.sconto import Sconto
from app.Models.promozione import Promozione
from app.Repos import offertaRepository as repo
from app.Repos import articoloRepository as repoA

def valida_date(data_inizio, data_fine):
    if data_inizio >= data_fine:
        raise ValueError("La data di inizio deve essere precedente alla data di fine.")


def visualizza_sconti():
    return repo.
    return repo.tutti_gli_sconti()
