from app.Repos.catalogoOfferte import CatalogoOfferte
from app.Repos.catalogoArticoli import CatalogoArticoli

class GestoreOfferte:
    @classmethod
    def visualizzaScontiAttivi(cls):
        return CatalogoOfferte.cercaSconti()

    @classmethod
    def creaSconto(cls, dati):
        if not cls.validaDatiSconto(dati):
            raise ValueError("Dati sconto non validi.")
        sconto = CatalogoOfferte.salvaSconto(dati)
        sconto_id = sconto.id
        articolo_id = dati.get("articolo_id")
        if articolo_id is not None:
            articolo = CatalogoArticoli.trovaPerId(articolo_id)
            if articolo is None:
                raise ValueError(f"Articolo con id={articolo_id} non trovato.")
            CatalogoArticoli.associaScontoAdArticolo(
                articolo,
                sconto,
                percentuale=dati.get("percentuale"),
                dataInizio=dati.get("dataInizio"),
                dataFine=dati.get("dataFine"),
            )
        return sconto_id

    @classmethod
    def validaDatiSconto(cls, dati):
        return (
            dati.get("percentuale") is not None
            and dati.get("dataInizio")
            and dati.get("dataFine")
            and dati["dataInizio"] <= dati["dataFine"]
        )

    @classmethod
    def validaDatiPromozione(cls, dati):
        return (
            dati.get("descrizione")
            and dati.get("dataInizio")
            and dati.get("dataFine")
            and dati["dataInizio"] <= dati["dataFine"]
        )

    @classmethod
    def creaPromozione(cls, dati):
        if not cls.validaDatiPromozione(dati):
            raise ValueError("Dati promozione non validi.")
        return CatalogoOfferte.salvaPromozione(dati)

    @classmethod
    def eliminaOfferta(cls, id, tipo):
        if tipo == "sconto":
            for articolo in CatalogoOfferte.getArticoliAssociati(id, "sconto"):
                CatalogoArticoli.rimuoviRiferimentoOfferta(articolo)
            CatalogoOfferte.rimuoviSconto(id)
        elif tipo == "promozione":
            for articolo in CatalogoOfferte.getArticoliAssociati(id, "promozione"):
                CatalogoArticoli.rimuoviRiferimentoOfferta(articolo)
            CatalogoOfferte.rimuoviPromozione(id)
        else:
            raise ValueError(f"Tipo offerta non valido: {tipo}")

    @classmethod
    def aggiornaListaSconti(cls):
        return cls.visualizzaScontiAttivi()

    @classmethod
    def aggiornaListaOfferte(cls):
        return cls.visualizzaOfferteAttive()

    @classmethod
    def visualizzaOfferteAttive(cls):
        return CatalogoOfferte.recuperaOfferteAttive()
