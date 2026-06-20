import csv
import os
from datetime import date, timedelta, time
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
            if cls.trovaFascePerData(giorno):
                date_libere.append(giorno.isoformat())
        return date_libere

    @classmethod
    def trovaFascePerData(cls, data):
        data_str = data.isoformat() if isinstance(data, date) else str(data)
        
        data_obj = None
        if isinstance(data, date):
            data_obj = data
        elif isinstance(data, str):
            try:
                data_obj = date.fromisoformat(data)
            except Exception:
                pass
                
        # Orari di apertura/chiusura
        apertura = None
        chiusura = None
        if data_obj:
            from app.Repos.orarioRepository import OrarioRepository
            
            def weekday_it(d):
                mapping = {
                    0: "Lunedì",
                    1: "Martedì",
                    2: "Mercoledì",
                    3: "Giovedì",
                    4: "Venerdì",
                    5: "Sabato",
                    6: "Domenica"
                }
                return mapping[d.weekday()]
                
            o_spec = OrarioRepository.cercaOrarioPerData(data_obj)
            if o_spec:
                apertura = o_spec.apertura
                chiusura = o_spec.chiusura
            else:
                giorno_sett = weekday_it(data_obj)
                o_sett = OrarioRepository.cercaOrarioPerGiorno(giorno_sett)
                if o_sett:
                    apertura = o_sett.apertura
                    chiusura = o_sett.chiusura

        def parse_time(t_str):
            if not t_str:
                return None
            try:
                parts = t_str.split(":")
                h = int(parts[0])
                m = int(parts[1]) if len(parts) > 1 else 0
                return time(h, m)
            except Exception:
                return None

        t_apertura = parse_time(apertura)
        t_chiusura = parse_time(chiusura)

        # Genera fasce disponibili di default basate sull'orario del negozio
        if not t_apertura or not t_chiusura:
            fasce_disponibili = [
                "09:00", "10:00", "11:00", "12:00",
                "15:00", "16:00", "17:00", "18:00", "19:00"
            ]
        else:
            fasce_disponibili = []
            for h in range(24):
                slot_t = time(h, 0)
                if t_apertura <= slot_t <= t_chiusura:
                    fasce_disponibili.append(f"{h:02d}:00")

        # Legge gli slot salvati nel file CSV per questa data
        slot_salvati = [s for s in cls.leggi() if s.data == data_str]
        ore_non_disponibili = {s.fasciaOraria for s in slot_salvati if not s.disponibile}
        ore_disponibili_salvate = {s.fasciaOraria for s in slot_salvati if s.disponibile}

        # Combina le fasce disponibili
        fasce_totali = []
        for f in fasce_disponibili:
            if f not in ore_non_disponibili:
                fasce_totali.append(f)
        for f in ore_disponibili_salvate:
            if f not in fasce_totali:
                fasce_totali.append(f)

        return sorted(list(set(fasce_totali)))

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
