import csv
import os
from datetime import date
from app.Models.promozione import Promozione
from app.Models.sconto import Sconto
from app.Models.offerte import Offerte
from app.Repos.catalogoArticoli import CatalogoArticoli

class CatalogoOfferte:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE = os.path.join(BASE_DIR, "Data", "offerte.csv")
    COLONNE = ["id", "tipo", "dataInizio", "dataFine", "descrizione", "percentuale", "evento"]

    @classmethod
    def leggi(cls):
        if not os.path.exists(cls.FILE):
            return []
        with open(cls.FILE, newline="", encoding="utf-8") as f:
            offerte = []
            for r in csv.DictReader(f):
                if r["tipo"] == "promozione":
                    offerte.append(Promozione(
                        id=int(r["id"]),
                        descrizione=r.get("descrizione", ""),
                        dataInizio=r["dataInizio"],
                        dataFine=r["dataFine"],
                    ))
                elif r["tipo"] == "sconto":
                    offerte.append(Sconto(
                        id=int(r["id"]),
                        evento=r.get("evento", ""),
                        percentuale=float(r["percentuale"]) if r.get("percentuale") else 0.0,
                        dataInizio=r["dataInizio"],
                        dataFine=r["dataFine"],
                    ))
                else:
                    offerte.append(Offerte(
                        id=int(r["id"]),
                        dataInizio=r["dataInizio"],
                        dataFine=r["dataFine"],
                    ))
            return offerte

    @classmethod
    def scrivi(cls, offerte):
        os.makedirs(os.path.dirname(cls.FILE), exist_ok=True)
        with open(cls.FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cls.COLONNE)
            w.writeheader()
            for o in offerte:
                riga = {
                    "id": o.id,
                    "tipo": getattr(o, "tipo", "offerta"),
                    "dataInizio": o.dataInizio,
                    "dataFine": o.dataFine,
                    "descrizione": "",
                    "percentuale": "",
                    "evento": "",
                }
                if isinstance(o, Promozione):
                    riga["descrizione"] = o.descrizione
                elif isinstance(o, Sconto):
                    riga["percentuale"] = o.percentuale
                    riga["evento"] = o.evento
                w.writerow(riga)

    @classmethod
    def salva(cls, offerta):
        tutte = cls.leggi()
        if offerta.id is None:
            offerta.id = max((o.id for o in tutte), default=0) + 1
            tutte.append(offerta)
        else:
            tutte = [offerta if o.id == offerta.id else o for o in tutte]
        cls.scrivi(tutte)
        return offerta

    @classmethod
    def salvaSconto(cls, dati):
        sconto = Sconto(
            evento=dati.get("evento", ""),
            percentuale=float(dati.get("percentuale", 0)),
            dataInizio=dati["dataInizio"],
            dataFine=dati["dataFine"],
        )
        return cls.salva(sconto)

    @classmethod
    def salvaPromozione(cls, dati):
        promozione = Promozione(
            descrizione=dati.get("descrizione", ""),
            dataInizio=dati["dataInizio"],
            dataFine=dati["dataFine"],
        )
        return cls.salva(promozione)

    @classmethod
    def cercaSconti(cls):
        return [o for o in cls.leggi() if isinstance(o, Sconto)]

    @classmethod
    def rimuoviSconto(cls, id):
        cls.scrivi([o for o in cls.leggi() if not (isinstance(o, Sconto) and o.id == id)])

    @classmethod
    def cercaPromozioni(cls):
        return [o for o in cls.leggi() if isinstance(o, Promozione)]

    @classmethod
    def cercaPromozione(cls, id):
        for o in cls.leggi():
            if isinstance(o, Promozione) and o.id == id:
                return o
        return None

    @classmethod
    def rimuoviPromozione(cls, id):
        cls.scrivi([o for o in cls.leggi() if not (isinstance(o, Promozione) and o.id == id)])

    @classmethod
    def getArticoliAssociati(cls, offertaId, tipo):
        if tipo == "sconto":
            sconto = next((o for o in cls.cercaSconti() if o.id == offertaId), None)
            if sconto is None:
                return []
            return [a for a in CatalogoArticoli.mostraCatalogo() if a.percentuale == sconto.percentuale]
        return CatalogoArticoli.mostraCatalogo()

    @classmethod
    def _offerte_valide(cls, data_riferimento=None):
        data_riferimento = data_riferimento or date.today().isoformat()
        return [
            o for o in cls.leggi()
            if o.dataInizio <= data_riferimento <= o.dataFine
        ]

    @classmethod
    def cercaOfferteValide(cls):
        return [o for o in cls._offerte_valide() if isinstance(o, Promozione)]

    @classmethod
    def recuperaOfferteAttive(cls):
        return cls.cercaOfferteValide()

    # Aliases
    @classmethod
    def salva_offerta(cls, offerta):
        return cls.salva(offerta)

    @classmethod
    def trova_offerta(cls, id):
        return next((o for o in cls.leggi() if o.id == id), None)

    @classmethod
    def trovaPerId(cls, id):
        return cls.trova_offerta(id)

    @classmethod
    def promozioni(cls):
        return cls.cercaPromozioni()

    @classmethod
    def sconti(cls):
        return cls.cercaSconti()

    @classmethod
    def elimina_offerta(cls, id):
        cls.scrivi([o for o in cls.leggi() if o.id != id])

    @classmethod
    def offerte_attive(cls, data_riferimento=None):
        return cls._offerte_valide(data_riferimento)

    @classmethod
    def tutti_gli_sconti(cls):
        return cls.cercaSconti()