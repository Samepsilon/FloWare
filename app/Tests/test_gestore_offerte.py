import unittest
from app.Services.gestoreOfferte import GestoreOfferte


class TestGestoreOfferte(unittest.TestCase):

    #validaDatiSconto

    def test_sconto_valido(self):
        dati = {"percentuale": 10, "dataInizio": "2026-06-01", "dataFine": "2026-06-30"}
        self.assertTrue(GestoreOfferte.validaDatiSconto(dati))

    def test_sconto_percentuale_zero(self):
        dati = {"percentuale": 0, "dataInizio": "2026-06-01", "dataFine": "2026-06-30"}
        self.assertTrue(GestoreOfferte.validaDatiSconto(dati))

    def test_sconto_senza_percentuale(self):
        dati = {"dataInizio": "2026-06-01", "dataFine": "2026-06-30"}
        self.assertFalse(GestoreOfferte.validaDatiSconto(dati))

    def test_sconto_senza_data_inizio(self):
        dati = {"percentuale": 10, "dataFine": "2026-06-30"}
        self.assertFalse(GestoreOfferte.validaDatiSconto(dati))

    def test_sconto_senza_data_fine(self):
        dati = {"percentuale": 10, "dataInizio": "2026-06-01"}
        self.assertFalse(GestoreOfferte.validaDatiSconto(dati))

    def test_sconto_date_invertite(self):
        dati = {"percentuale": 10, "dataInizio": "2026-06-30", "dataFine": "2026-06-01"}
        self.assertFalse(GestoreOfferte.validaDatiSconto(dati))


    #validaDatiPromozione

    def test_promozione_valida(self):
        dati = {"descrizione": "Saldi estivi", "dataInizio": "2026-07-01", "dataFine": "2026-07-31"}
        self.assertTrue(GestoreOfferte.validaDatiPromozione(dati))

    def test_promozione_date_uguali(self):
        dati = {"descrizione": "Flash sale", "dataInizio": "2026-07-15", "dataFine": "2026-07-15"}
        self.assertTrue(GestoreOfferte.validaDatiPromozione(dati))

    def test_promozione_senza_descrizione(self):
        dati = {"dataInizio": "2026-07-01", "dataFine": "2026-07-31"}
        self.assertFalse(GestoreOfferte.validaDatiPromozione(dati))


    def test_promozione_date_invertite(self):
        dati = {"descrizione": "Promo", "dataInizio": "2026-07-31", "dataFine": "2026-07-01"}
        self.assertFalse(GestoreOfferte.validaDatiPromozione(dati))



if __name__ == "__main__":
    unittest.main()
