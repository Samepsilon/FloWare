from app.Repos.catalogoOfferte import CatalogoOfferte

class SistemaOfferte:
    @classmethod
    def recuperaOfferteAttive(cls):
        return CatalogoOfferte.recuperaOfferteAttive()

    @classmethod
    def visualizzaOfferteAttive(cls):
        return cls.recuperaOfferteAttive()
