
class Notifica:
    def __init__(self, destinatario, messaggio, letta, tipo, richiestaId = None, id = None):
        self.id = id
        self.destinatario = destinatario
        self.messaggio = messaggio
        self.letta = letta
        self.tipo = tipo
        self.richiestaId = richiestaId
