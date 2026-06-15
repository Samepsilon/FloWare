from app.Repos import orarioRepository as repo


def visualizzaOrari():
    return repo.cercaOrari()


def aggiornaOrarioSettimanale(giorno, nuoviOrari):
    if not validaOrario(nuoviOrari):
        raise ValueError("Orario non valido.")
    esistente = repo.cercaOrarioPerGiorno(giorno)
    if esistente:
        return repo.aggiornaOrario(esistente.id, nuoviOrari)
    return repo.nuovoOrario(giorno, nuoviOrari, tipo="settimanale")


def validaOrario(nuoviOrari):
    dati = nuoviOrari if isinstance(nuoviOrari, dict) else {}
    return bool(dati.get("apertura") and dati.get("chiusura"))


def impostaChiusuraStraordinaria(data):
    return repo.nuovoOrario(
        giorno=None,
        nuoviOrari={"apertura": "", "chiusura": "", "dataSpecifica": str(data)},
        tipo="chiusura",
    )


def impostaOrarioTemporaneo(data, orario):
    dati = orario if isinstance(orario, dict) else {}
    dati["dataSpecifica"] = str(data)
    return repo.nuovoOrario(giorno=None, nuoviOrari=dati, tipo="speciale")


def aggiornaVisualizzazioneOrari():
    return visualizzaOrari()
