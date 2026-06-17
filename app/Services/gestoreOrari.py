from app.Repos.orarioRepository import OrarioRepository

class GestoreOrari:
    @classmethod
    def visualizzaOrari(cls):
        return OrarioRepository.cercaOrari()

    @classmethod
    def aggiornaOrarioSettimanale(cls, giorno, nuoviOrari):
        if not cls.validaOrario(nuoviOrari):
            raise ValueError("Orario non valido.")
        esistente = OrarioRepository.cercaOrarioPerGiorno(giorno)
        if esistente:
            return OrarioRepository.aggiornaOrario(esistente.id, nuoviOrari)
        return OrarioRepository.nuovoOrario(giorno, nuoviOrari, tipo="settimanale")

    @classmethod
    def validaOrario(cls, nuoviOrari):
        dati = nuoviOrari if isinstance(nuoviOrari, dict) else {}
        return bool(dati.get("apertura") and dati.get("chiusura"))

    @classmethod
    def impostaChiusuraStraordinaria(cls, data):
        return OrarioRepository.nuovoOrario(
            giorno=None,
            nuoviOrari={"apertura": "", "chiusura": "", "dataSpecifica": str(data)},
            tipo="chiusura",
        )

    @classmethod
    def impostaOrarioTemporaneo(cls, data, orario):
        dati = orario if isinstance(orario, dict) else {}
        dati["dataSpecifica"] = str(data)
        return OrarioRepository.nuovoOrario(giorno=None, nuoviOrari=dati, tipo="speciale")

    @classmethod
    def aggiornaVisualizzazioneOrari(cls):
        return cls.visualizzaOrari()
