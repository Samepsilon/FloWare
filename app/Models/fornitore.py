
class Fornitore:

    def __init__(self, nome, contatti, tipologiaMerce, servizioDomicilio=False, id=None):
        self.id = id
        self.nome = nome
        self.contatti = contatti
        self.tipologiaMerce = tipologiaMerce
        self.servizioDomicilio = servizioDomicilio

    def aggiornaProprieta(self, nuoviDati):
        for chiave, valore in nuoviDati.items():
            if hasattr(self, chiave):
                setattr(self, chiave, valore)

    """
    @staticmethod
    def findAll():
        from app.Repos import fornitoreRepository as repo
        return repo.cercaFornitori()

    def find(self):
        from app.Repos import fornitoreRepository as repo
        return repo.cercaFornitore(self)
        
    """
    def __repr__(self):
        return str({
            "id": self.id,
            "nome": self.nome,
            "contatti": self.contatti,
            "tipologiaMerce": self.tipologiaMerce,
            "servizioDomicilio": self.servizioDomicilio,
        })
