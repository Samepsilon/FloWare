
class Consegna:

    def __init__(self, regione, citta, via, civico, stato = None , clienteId = None, id = None):
        self.id = id
        self.regione = regione
        self.citta = citta
        self.via = via
        self.civico = civico
        self.stato = stato
        self.clienteId = clienteId 

    def __repr__(self):
        stato_str = f", stato='{self.stato}'" if self.stato else ""  # ← 4 spazi
        return f"[{self.id}] {self.via} {self.civico}, {self.citta} ({self.regione}){stato_str}"

    def getStato(self):
        return self.stato
    
    def setStato(self, nuovo_stato: str) -> None:
        if not isinstance(nuovo_stato, str) and nuovo_stato is not None:
            raise TypeError("stato deve essere stringa o None")
        self.stato = nuovo_stato
    
    def getClienteId(self):
        return self.clienteId
