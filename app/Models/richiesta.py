from datetime import date

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

    # +getDataOra() : String
    def getDataOra(self):
        # Se data è un oggetto date, lo formattiamo, altrimenti lo usiamo direttamente
        data_str = self.data.strftime("%d/%m/%Y") if hasattr(self.data, 'strftime') else str(self.data)
        return f"{data_str} {self.ora}"