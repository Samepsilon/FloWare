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
    
    def getDataOra(self) -> str:
        """Restituisce data e ora formattate come stringa"""
        # Se data è un oggetto date
        if hasattr(self.data, 'strftime'):
            data_str = self.data.strftime("%d/%m/%Y")
        else:
            data_str = str(self.data)
        
        # Se ora è un oggetto time
        if hasattr(self.ora, 'strftime'):
            ora_str = self.ora.strftime("%H:%M")
        else:
            ora_str = str(self.ora)
        
        return f"{data_str} {ora_str}"

