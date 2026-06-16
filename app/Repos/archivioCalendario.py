import csv
import os
from datetime import date, timedelta
from app.Models.slotOrario import SlotOrario

BASE_DIR = os.path.abspath("..")
FILE = BASE_DIR + "/Data/slot_orari.csv"

COLONNE = ["id", "data", "fasciaOraria", "disponibile"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        righe = []
        for r in csv.DictReader(f):
            righe.append(SlotOrario(
                id=int(r["id"]),
                data=r["data"],
                fasciaOraria=r["fasciaOraria"],
                disponibile=r["disponibile"] == "True",
            ))
        return righe


def scrivi(slot_orari):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNE)
        w.writeheader()
        for s in slot_orari:
            w.writerow({
                "id": s.id,
                "data": s.data,
                "fasciaOraria": s.fasciaOraria,
                "disponibile": s.disponibile,
            })


def salva(slot_orario):
    tutti = leggi()
    if slot_orario.id is None:
        slot_orario.id = max((s.id for s in tutti), default=0) + 1
        tutti.append(slot_orario)
    else:
        tutti = [slot_orario if s.id == slot_orario.id else s for s in tutti]
    scrivi(tutti)
    return slot_orario


def trovaDateLibere(giorni=30):
    oggi = date.today()
    date_libere = []
    for i in range(giorni):
        giorno = oggi + timedelta(days=i)
        data_str = giorno.isoformat()
        slot_giorno = [s for s in leggi() if s.data == data_str]
        if not slot_giorno or any(s.disponibile for s in slot_giorno):
            date_libere.append(data_str)
    return date_libere


def trovaFascePerData(data):
    data_str = data.isoformat() if isinstance(data, date) else str(data)
    return [s.fasciaOraria for s in leggi() if s.data == data_str and s.disponibile]


def salvaScelta(data, ora):
    data_str = data.isoformat() if isinstance(data, date) else str(data)
    for s in leggi():
        if s.data == data_str and s.fasciaOraria == ora:
            s.disponibile = False
            return _salva(s)
    slot = SlotOrario(data=data_str, fasciaOraria=ora, disponibile=False)
    return salva(slot)


def trovaPerId(id):
    for s in leggi():
        if s.id == id:
            return s
    return None


