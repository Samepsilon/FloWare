import csv
import os
from datetime import datetime, date, time
from app.Models.slotOrario import SlotOrario

FILE = "data/slot_orari.csv"
COLONNE = ["id", "data", "ora_inizio", "ora_fine", "disponibile"]


def leggi():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        righe = []
        for r in csv.DictReader(f):
            data_obj = datetime.strptime(r["data"], "%Y-%m-%d").date()
            ora_inizio_obj = datetime.strptime(r["ora_inizio"], "%H:%M").time()
            ora_fine_obj = datetime.strptime(r["ora_fine"], "%H:%M").time()
            
            righe.append(SlotOrario(
                id=int(r["id"]),
                data=data_obj,
                ora_inizio=ora_inizio_obj,
                ora_fine=ora_fine_obj,
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
                "data": s.data.strftime("%Y-%m-%d"),
                "ora_inizio": s.ora_inizio.strftime("%H:%M"),
                "ora_fine": s.ora_fine.strftime("%H:%M"),
                "disponibile": s.disponibile,
            })


def salva_slot_orario(slot_orario):
    tutti = leggi()
    if slot_orario.id is None:
        slot_orario.id = max((s.id for s in tutti), default=0) + 1
        tutti.append(slot_orario)
    else:
        tutti = [slot_orario if s.id == slot_orario.id else s for s in tutti]
    scrivi(tutti)
    return slot_orario


def trova_slot_orario(id):
    for s in leggi():
        if s.id == id:
            return s
    return None


def trovaPerId(id):
    return trova_slot_orario(id)



def date_libere(data_inizio: date, data_fine: date) -> list:
    tutti = leggi()
    date_occupate = {s.data for s in tutti if not s.disponibile}
    
    libere = []
    giorno = data_inizio
    while giorno <= data_fine:
        if giorno not in date_occupate:
            libere.append(giorno)
        giorno = date(giorno.year, giorno.month, giorno.day + 1)
    return libere


def slot_liberi_per_data(data: date) -> list:
    return [s for s in leggi() if s.data == data and s.disponibile]


def verifica_disponibilita(data: date, ora_inizio: time, ora_fine: time) -> bool:
    for s in leggi():
        if s.data == data and s.ora_inizio == ora_inizio and s.ora_fine == ora_fine:
            return s.disponibile
    return False  # slot non esiste


def occupa_slot(data: date, ora_inizio: time, ora_fine: time) -> bool:
    for s in leggi():
        if s.data == data and s.ora_inizio == ora_inizio and s.ora_fine == ora_fine:
            s.disponibile = False
            salva_slot_orario(s)
            return True
    return False


def libera_slot(data: date, ora_inizio: time, ora_fine: time) -> bool:
    for s in leggi():
        if s.data == data and s.ora_inizio == ora_inizio and s.ora_fine == ora_fine:
            s.disponibile = True
            salva_slot_orario(s)
            return True
    return False


def elimina_slot_orario(id):
    tutti = leggi()
    filtrati = [s for s in tutti if s.id != id]
    scrivi(filtrati)


def elimina_slot_per_data(data):
    tutti = leggi()
    filtrati = [s for s in tutti if s.data != data]
    scrivi(filtrati)