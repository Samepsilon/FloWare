TIPI_VALIDI = ["preventivo", "appuntamento"]
STATI_VALIDI = ["in attesa", "confermata", "annullata"]


class Richiesta:

    def __init__(self, tipo, stato="in attesa", data="", ora="", contatti="", descrizione="", clienteId=None, id=None):
        self.id = id
        self.tipo = tipo
        self.stato = stato
        self.data = data
        self.ora = ora
        self.contatti = contatti
        self.descrizione = descrizione
        self.clienteId = clienteId

    def setStato(self, stato):
        self.stato = stato

    def getStato(self):
        return self.stato

    def getDataOra(self):
        return f"{self.data} {self.ora}".strip()
