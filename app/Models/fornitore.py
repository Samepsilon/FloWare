

class Fornitore:
    def __init__(self, nome, contatti, tipologia, domicilio=False, id=None):
        self.id = id
        self.nome = nome
        self.contatti = contatti
        self.tipologia = tipologia
        self.domicilio = domicilio

    def __repr__(self):
        domicilio_str = "sì" if self.domicilio else "no"
        return f"[{self.id}] {self.nome} | {self.tipologia} | {self.contatti} | domicilio: {domicilio_str}"
