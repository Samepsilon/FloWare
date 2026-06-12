

class Fornitore:
    def __init__(self, nome, contatti, tipologia, servizioDomicilio=False, id=None):
        self.id = id
        self.nome = nome
        self.contatti = contatti
        self.tipologia = tipologia
        self.servizioDomicilio = servizioDomicilio

    def __repr__(self):
        domicilio_str = "sì" if self.domicilio else "no"
        return f"[{self.id}] {self.nome} | {self.tipologia} | {self.contatti} | servizioDomicilio: {domicilio_str}"
