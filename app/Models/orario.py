
class Orario:

    def __init__(self, giorno, apertura, chiusura, tipo, dataSpecifica=None, id=None):
        self.id = id
        self.giorno = giorno
        self.apertura = apertura
        self.chiusura = chiusura
        self.tipo = tipo
        self.dataSpecifica = dataSpecifica

    def __repr__(self):
        return str({
            "id": self.id,
            "giorno": self.giorno,
            "apertura": self.apertura,
            "chiusura": self.chiusura,
            "tipo": self.tipo,
            "dataSpecifica": self.dataSpecifica,
        })

    def getDettagliOrario(self) -> str:
        if not self.apertura or not self.chiusura:
            return "Orario non impostato"

        if self.tipo == "settimanale":
            return f"{self.giorno}: {self.apertura} - {self.chiusura}"
        if self.tipo == "speciale":
            return f"{self.dataSpecifica}: {self.apertura} - {self.chiusura}"
        return f"{self.apertura} - {self.chiusura}"


    def aggiornaOrario(self,nuovaApertura = None, nuovaChiusura = None):
        if nuovaApertura != None:
            self.apertura = nuovaApertura
        if nuovaChiusura != None:
            self.chiusura = nuovaChiusura




