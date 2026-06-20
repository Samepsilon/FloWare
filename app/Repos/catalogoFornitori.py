import csv
import os
from app.Models.fornitore import Fornitore

class CatalogoFornitori:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE = os.path.join(BASE_DIR, "Data", "fornitori.csv")
    COLONNE = ["id", "nome", "contatti", "tipologia", "servizioDomicilio"]

    @classmethod
    def leggi(cls):
        if not os.path.exists(cls.FILE):
            return []
        with open(cls.FILE, newline="", encoding="utf-8") as f:
            righe = []
            for r in csv.DictReader(f):
                righe.append(Fornitore(
                    id=int(r["id"]),
                    nome=r["nome"],
                    contatti=r["contatti"],
                    tipologiaMerce=r["tipologia"],
                    servizioDomicilio=r["servizioDomicilio"] == "True",
                ))
            return righe

    @classmethod
    def scrivi(cls, fornitori):
        os.makedirs(os.path.dirname(cls.FILE), exist_ok=True)
        with open(cls.FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cls.COLONNE)
            w.writeheader()
            for f_ in fornitori:
                w.writerow({
                    "id": f_.id,
                    "nome": f_.nome,
                    "contatti": f_.contatti,
                    "tipologia": f_.tipologiaMerce,
                    "servizioDomicilio": f_.servizioDomicilio,
                })

    @classmethod
    def salvaFornitore(cls, fornitore):
        tutti = cls.leggi()
        if fornitore.id is None:
            fornitore.id = max((f.id for f in tutti), default=0) + 1
            tutti.append(fornitore)
        else:
            tutti = [fornitore if f.id == fornitore.id else f for f in tutti]
        cls.scrivi(tutti)
        return fornitore

    @classmethod
    def cercaFornitori(cls, id):
        for f in cls.leggi():
            if f.id == id:
                return f
        return None

    # Alias: trovaPerId
    @classmethod
    def trovaPerId(cls, id):
        return cls.cercaFornitori(id)

    @classmethod
    def caricaListaFornitori(cls):
        return cls.leggi()

    @classmethod
    def cercaFornitore(cls, Nome):
        for f in cls.leggi():
            if f.nome == Nome:
                return f
        return None

    @classmethod
    def aggiornaFornitore(cls, id, dati):
        fornitore = cls.cercaFornitori(id)
        if fornitore is None:
            return None
        fornitore.aggiornaProprieta(dati)
        return cls.salvaFornitore(fornitore)

    @classmethod
    def rimuoviFornitore(cls, fornitore):
        id_fornitore = fornitore if isinstance(fornitore, int) else fornitore.id
        cls.scrivi([f for f in cls.leggi() if f.id != id_fornitore])
