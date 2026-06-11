import csv
import os
from app.Models.promozione import Promozione
from app.Models.sconto import Sconto

FILE = "data/offerte.csv"
COLONNE = ["id", "tipo", "dataInizio", "dataFine", "descrizione", "percentuale", "prodottoId"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        offerte = []
        for r in csv.DictReader(f):
            if r["tipo"] == "promozione":
                offerte.append(Promozione(
                    id=int(r["id"]),
                    dataInizio=r["dataInizio"],
                    dataFine=r["dataFine"],
                    descrizione=r["descrizione"],
                ))
            elif r["tipo"] == "sconto":
                offerte.append(Sconto(
                    id=int(r["id"]),
                    dataInizio=r["dataInizio"],
                    dataFine=r["dataFine"],
                    percentuale=float(r["percentuale"]),
                    prodottoId=int(r["prodottoId"]) if r["prodottoId"] else None,
                ))
            else:
                offerte.append(Offerta(
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
                "tipo": o.tipo,
                "dataInizio": o.dataInizio,
                "dataFine": o.dataFine,
                "descrizione": "",
                "percentuale": "",
                "prodottoId": "",
            }
            
            if o.tipo == "promozione":
                riga["descrizione"] = o.descrizione
            elif o.tipo == "sconto":
                riga["percentuale"] = o.percentuale
                riga["prodottoId"] = o.prodottoId if o.prodottoId is not None else ""
            
            w.writerow(riga)


def salva_offerta(offerta):
    tutte = leggi()
    if offerta.id is None:
        offerta.id = max((o.id for o in tutte), default=0) + 1
        tutte.append(offerta)
    else:
        tutte = [offerta if o.id == offerta.id else o for o in tutte]
    scrivi(tutte)
    return offerta


def trova_offerta(id):
    for o in leggi():
        if o.id == id:
            return o
    return None


def trovaPerId(id):
    return trova_offerta(id)


def offerte_attive(data_riferimento):
    """Restituisce le offerte attive in una data specifica"""
    return [o for o in leggi() if o.dataInizio <= data_riferimento <= o.dataFine]


def offerte_per_tipo(tipo):
    """Filtra per tipo: 'promozione', 'sconto', 'offerta'"""
    return [o for o in leggi() if o.tipo == tipo]


def promozioni():
    return [o for o in leggi() if o.tipo == "promozione"]


def sconti():
    return [o for o in leggi() if o.tipo == "sconto"]


def elimina_offerta(id):
    tutte = leggi()
    filtrati = [o for o in tutte if o.id != id]
    scrivi(filtrati)