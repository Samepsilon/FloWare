from app.Repos import catalogoOfferte as repo


def recuperaOfferteAttive():
    return repo.recuperaOfferteAttive()


def visualizzaOfferteAttive():
    return recuperaOfferteAttive()
