class Fornitore:
    
    def __init__(self, nome, contatti, tipologiaMerce, servizioDomicilio=False, id=None):
        self.id = id
        self.nome = nome
        self.contatti = contatti
        self.tipologiaMerce = tipologiaMerce
        self.servizioDomicilio = servizioDomicilio

    def __repr__(self):
        domicilio_str = "sì" if self.servizioDomicilio else "no"
        return f"[{self.id}] {self.nome} | {self.tipologiaMerce} | {self.contatti} | servizioDomicilio: {domicilio_str}"
