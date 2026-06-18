"""
Questo modulo gestisce l'accesso da parte dei clienti alle offerte attive,
consentendo il recupero e la visualizzazione di sconti e promozioni.
"""

from app.Repos.catalogoOfferte import CatalogoOfferte

class SistemaOfferte:
    @classmethod
    def recuperaOfferteAttive(cls):
        return CatalogoOfferte.recuperaOfferteAttive()

    @classmethod
    def visualizzaOfferteAttive(cls):
        return cls.recuperaOfferteAttive()
