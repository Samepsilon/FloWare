import csv
import os
from datetime import date, timedelta
from app.Models.slotOrario import SlotOrario

class ArchivioCalendario:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE = os.path.join(BASE_DIR, "Data", "slot_orari.csv")
    COLONNE = ["id", "data", "fasciaOraria", "disponibile"]

    @classmethod
    def leggi(cls):
        if not os.path.exists(cls.FILE):
            return []
        with open(cls.FILE, newline="", encoding="utf-8") as f:
            righe = []
            for r in csv.DictReader(f):
                righe.append(SlotOrario(
                    id=int(r["id"]),
                    data=r["data"],
                    fasciaOraria=r["fasciaOraria"],
                    disponibile=r["disponibile"] == "True",
                ))
            return righe

    @classmethod
    def scrivi(cls, slot_orari):
        os.makedirs(os.path.dirname(cls.FILE), exist_ok=True)
        with open(cls.FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cls.COLONNE)
            w.writeheader()
            for s in slot_orari:
                w.writerow({
                    "id": s.id,
                    "data": s.data,
                    "fasciaOraria": s.fasciaOraria,
                    "disponibile": s.disponibile,
                })

    @classmethod
    def salva(cls, slot_orario):
        tutti = cls.leggi()
        if slot_orario.id is None:
            slot_orario.id = max((s.id for s in tutti), default=0) + 1
            tutti.append(slot_orario)
        else:
            tutti = [slot_orario if s.id == slot_orario.id else s for s in tutti]
        cls.scrivi(tutti)
        return slot_orario

    @classmethod
    def trovaDateLibere(cls, giorni=30):
        oggi = date.today()
        date_libere = []
        for i in range(giorni):
            giorno = oggi + timedelta(days=i)
            data_str = giorno.isoformat()
            slot_giorno = [s for s in cls.leggi() if s.data == data_str]
            if not slot_giorno or any(s.disponibile for s in slot_giorno):
                date_libere.append(data_str)
        return date_libere

    @classmethod
    def trovaFascePerData(cls, data):
        data_str = data.isoformat() if isinstance(data, date) else str(data)
        return [s.fasciaOraria for s in cls.leggi() if s.data == data_str and s.disponibile]

    @classmethod
    def salvaScelta(cls, data, ora):
        data_str = data.isoformat() if isinstance(data, date) else str(data)
        for s in cls.leggi():
            if s.data == data_str and s.fasciaOraria == ora:
                s.disponibile = False
                return cls.salva(s)
        slot = SlotOrario(data=data_str, fasciaOraria=ora, disponibile=False)
        return cls.salva(slot)

    @classmethod
    def trovaPerId(cls, id):
        for s in cls.leggi():
            if s.id == id:
                return s
        return None
