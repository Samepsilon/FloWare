import unittest
from app.Models.orario import Orario


class TestOrario(unittest.TestCase):

    def setUp(self):
        self.orario = Orario(
            giorno="Lunedì",
            apertura="08:00",
            chiusura="18:00",
            tipo="settimanale",
            dataSpecifica=None,
            id=1,
        )

    def test_id(self):
        self.assertEqual(self.orario.id, 1)

    def test_giorno(self):
        self.assertEqual(self.orario.giorno, "Lunedì")

    def test_apertura(self):
        self.assertEqual(self.orario.apertura, "08:00")

    def test_chiusura(self):
        self.assertEqual(self.orario.chiusura, "18:00")

    def test_tipo(self):
        self.assertEqual(self.orario.tipo, "settimanale")

    def test_data_specifica_none(self):
        self.assertIsNone(self.orario.dataSpecifica)

    #  Valori di default

    def test_default_data_specifica(self):
        o = Orario(giorno="Martedì", apertura="09:00", chiusura="17:00", tipo="settimanale")
        self.assertIsNone(o.dataSpecifica)


    #getDettagliOrario

    def test_dettagli_settimanale(self):
        risultato = self.orario.getDettagliOrario()
        self.assertEqual(risultato, "Lunedì: 08:00 - 18:00")

    def test_dettagli_speciale(self):
        o = Orario(giorno=None, apertura="10:00", chiusura="14:00", tipo="speciale", dataSpecifica="2026-12-25")
        risultato = o.getDettagliOrario()
        self.assertEqual(risultato, "2026-12-25: 10:00 - 14:00")


    def test_dettagli_orario_non_impostato_apertura_none(self):
        o = Orario(giorno="Lunedì", apertura=None, chiusura="18:00", tipo="settimanale")
        risultato = o.getDettagliOrario()
        self.assertEqual(risultato, "Orario non impostato")

    def test_dettagli_orario_non_impostato_chiusura_none(self):
        o = Orario(giorno="Lunedì", apertura="08:00", chiusura=None, tipo="settimanale")
        risultato = o.getDettagliOrario()
        self.assertEqual(risultato, "Orario non impostato")

    def test_dettagli_orario_entrambi_none(self):
        o = Orario(giorno="Lunedì", apertura=None, chiusura=None, tipo="settimanale")
        risultato = o.getDettagliOrario()
        self.assertEqual(risultato, "Orario non impostato")

    # aggiornaOrario

    def test_aggiorna_apertura(self):
        self.orario.aggiornaOrario(nuovaApertura="09:30")
        self.assertEqual(self.orario.apertura, "09:30")
        self.assertEqual(self.orario.chiusura, "18:00")  # invariata

    def test_aggiorna_chiusura(self):
        self.orario.aggiornaOrario(nuovaChiusura="20:00")
        self.assertEqual(self.orario.apertura, "08:00")  # invariata
        self.assertEqual(self.orario.chiusura, "20:00")

    # repr

    def test_repr_contiene_giorno(self):
        rappresentazione = repr(self.orario)
        self.assertIn("Lunedì", rappresentazione)

    def test_repr_contiene_apertura(self):
        rappresentazione = repr(self.orario)
        self.assertIn("08:00", rappresentazione)


if __name__ == "__main__":
    unittest.main()
