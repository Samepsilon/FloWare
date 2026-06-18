
class Orario:
     
    def __init__(self, giorno, apertura, chiusura, tipo, dataSpecifica, id = None)
          self.id = id
          self.giorno = giorno
          self.apertura = apertura
          self.chiusura = chiusura
          self.tipo = tipo
          self.dataSpecifica = dataSpecifica

    def getDettagliOrario(self) -> str:        
        if not self.apertura or not self.chiusura:
            return "Orario non impostato"
        
        if self.tipo == "settimanale":
            return f"{self.giorno}: {self.apertura} - {self.chiusura}"
        elif self.tipo == "speciale":
            return f"{self.dataSpecifica}: {self.apertura} - {self.chiusura}"
        else:
            return f"{self.apertura} - {self.chiusura}"
    
    def aggiornaOrario(self, apertura: str, chiusura: str) -> None:
        self.apertura = apertura
        self.chiusura = chiusura
    
    def __str__(self):
        return self.getDettagliOrario()
