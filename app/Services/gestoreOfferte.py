from app.Repos import catalogoOfferte as repo
from app.Repos import catalogoArticoli as repoA


def visualizzaScontiAttivi():
    return repo.cercaSconti()


def creaSconto(dati):
    if not validaDatiSconto(dati):
        raise ValueError("Dati sconto non validi.")
    sconto_id = repo.salvaSconto(dati)
    articolo_id = dati.get("articolo_id")
    if articolo_id is not None:
        articolo = repoA.trovaPerId(articolo_id)
        if articolo is None:
            raise ValueError(f"Articolo con id={articolo_id} non trovato.")
        sconto = next((s for s in repo.cercaSconti() if s.id == sconto_id), None)
        repoA.associaScontoAdArticolo(
            articolo,
            sconto,
            percentuale=dati.get("percentuale"),
            dataInizio=dati.get("dataInizio"),
            dataFine=dati.get("dataFine"),
        )
    return sconto_id


def validaDatiSconto(dati):
    return (
        dati.get("percentuale") is not None
        and dati.get("dataInizio")
        and dati.get("dataFine")
        and dati["dataInizio"] <= dati["dataFine"]
    )


def validaDatiPromozione(dati):
    return (
        dati.get("descrizione")
        and dati.get("dataInizio")
        and dati.get("dataFine")
        and dati["dataInizio"] <= dati["dataFine"]
    )


def creaPromozione(dati):
    if not validaDatiPromozione(dati):
        raise ValueError("Dati promozione non validi.")
    return repo.salvaPromozione(dati)


def eliminaOfferta(id, tipo):
    if tipo == "sconto":
        for articolo in repo.getArticoliAssociati(id, "sconto"):
            repoA.rimuoviRiferimentoOfferta(articolo)
        repo.rimuoviSconto(id)
    elif tipo == "promozione":
        for articolo in repo.getArticoliAssociati(id, "promozione"):
            repoA.rimuoviRiferimentoOfferta(articolo)
        repo.rimuoviPromozione(id)
    else:
        raise ValueError(f"Tipo offerta non valido: {tipo}")


def aggiornaListaSconti():
    return visualizzaScontiAttivi()


def aggiornaListaOfferte():
    return visualizzaOfferteAttive()


def visualizzaOfferteAttive():
    return repo.recuperaOfferteAttive()
