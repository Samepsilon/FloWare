
class Consegna:

    def __init__(self, regione, citta, via, civico, stato=None, clienteId=None, id=None):
        self.id = id
        self.regione = regione
        self.citta = citta
        self.via = via
        self.civico = civico
        self.stato = stato
        self.clienteId = clienteId

    def __repr__(self):
        return str({
            "id": self.id,
            "regione": self.regione,
            "citta": self.citta,
            "via": self.via,
            "civico": self.civico,
            "stato": self.stato,
            "clienteId": self.clienteId,
        })

    def getStato(self):
        return self.stato

    def setStato(self, nuovoStato):
        if nuovoStato is not None and not isinstance(nuovoStato, str):
            raise TypeError("stato deve essere stringa o None")
        self.stato = nuovoStato

    def getClienteId(self):
        return self.clienteId
