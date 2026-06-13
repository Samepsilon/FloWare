TIPI_VALIDI = ["preventivo", "appuntamento"]
STATI_VALIDI = ["in attesa", "confermata", "annullata"]

class Richiesta:

    def __init__(self, id, tipo, stato, data, ora, contatti, descrizione, clienteId):
        self.id = id
        self.tipo = tipo
        self.stato = stato
        self.data = data                  
        self.ora = ora                    
        self.contatti = contatti
        self.descrizione = descrizione
        self.clienteId = clienteId

    # +setStato(stato : String) : void
    def setStato(self, stato):
        self.stato = stato

    # +getStato() : String
    def getStato(self):
        return self.stato

