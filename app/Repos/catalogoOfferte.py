import csv
import os
from datetime import date
from app.Models.promozione import Promozione
from app.Models.sconto import Sconto
from app.Models.offerte import Offerte
from app.Repos import catalogoArticoli as repoArticoli

FILE = "data/offerte.csv"
COLONNE = ["id", "tipo", "dataInizio", "dataFine", "descrizione", "percentuale", "evento"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
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


def scrivi(offerte):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNE)
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


def salva(offerta):
    tutte = leggi()
    if offerta.id is None:
        offerta.id = max((o.id for o in tutte), default=0) + 1
        tutte.append(offerta)
    else:
        tutte = [offerta if o.id == offerta.id else o for o in tutte]
    scrivi(tutte)
    return offerta

def salvaSconto(dati):
    sconto = Sconto(
        evento=dati.get("evento", ""),
        percentuale=float(dati.get("percentuale", 0)),
        dataInizio=dati["dataInizio"],
        dataFine=dati["dataFine"],
    )
    return salva(sconto)

def salvaPromozione(dati):
    promozione = Promozione(
        descrizione=dati.get("descrizione", ""),
        dataInizio=dati["dataInizio"],
        dataFine=dati["dataFine"],
    )
    return salva(promozione)



def cercaSconti():
    return [o for o in leggi() if isinstance(o, Sconto)]


def rimuoviSconto(id):
    scrivi([o for o in leggi() if not (isinstance(o, Sconto) and o.id == id)])


def cercaPromozioni():
    return [o for o in leggi() if isinstance(o, Promozione)]


def cercaPromozione(id):
    for o in leggi():
        if isinstance(o, Promozione) and o.id == id:
            return o
    return None


def rimuoviPromozione(id):
    scrivi([o for o in leggi() if not (isinstance(o, Promozione) and o.id == id)])


def getArticoliAssociati(offertaId, tipo):
    if tipo == "sconto":
        sconto = next((o for o in cercaSconti() if o.id == offertaId), None)
        if sconto is None:
            return []
        return [a for a in repoArticoli.mostraCatalogo() if a.percentuale == sconto.percentuale]
    return repoArticoli.mostraCatalogo()


def _offerte_valide(data_riferimento=None):
    data_riferimento = data_riferimento or date.today().isoformat()
    return [
        o for o in leggi()
        if o.dataInizio <= data_riferimento <= o.dataFine
    ]


def cercaOfferteValide():
    return [o for o in _offerte_valide() if isinstance(o, Promozione)]


def recuperaOfferteAttive():
    return cercaOfferteValide()


# Alias di compatibilità
"""
salva_offerta = salva
trova_offerta = lambda id: next((o for o in leggi() if o.id == id), None)
trovaPerId = trova_offerta
promozioni = cercaPromozioni
sconti = cercaSconti
elimina_offerta = lambda id: scrivi([o for o in leggi() if o.id != id])
offerte_attive = _offerte_valide
tutti_gli_sconti = cercaSconti
"""