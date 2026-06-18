import json
import os
from PyQt5.QtWidgets import QApplication

# Configurazione dello Stile e Variabili Generali
IMPOSTAZIONI_STILE = {
    "background_color": "#fbfbfb",      # Sfondo principale
    "text_color": "#2c3e50",            # Testo principale (grigio scuro/blu cobalto)
    "primary_color": "#09BC8A",         # Colore primario per bottoni
    "primary_text": "#ffffff",          # Colore del testo sui bottoni primari
    "secondary_color": "#ecf0f1",       # Sfondi alternativi o bordi chiari
    "border_color": "#8A7E72",          # Colore dei bordi
    "font_family": "Segoe UI",          # Carattere predefinito
    "font_size": 10                     # Dimensione base del font (in punti)
}

CONFIG_FILE_PATH = "stile_utente.json"

def carica_stile():
    """Carica lo stile personalizzato da file JSON."""
    global IMPOSTAZIONI_STILE
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                dati = json.load(f)
                IMPOSTAZIONI_STILE.update(dati)
        except Exception:
            pass

def salva_stile():
    """Salva la configurazione corrente su file JSON."""
    try:
        with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(IMPOSTAZIONI_STILE, f, indent=4)
    except Exception:
        pass

def applica_stile_globale():
    """Genera e applica lo stylesheet QSS all'intera applicazione PyQt5."""
    app = QApplication.instance()
    if app:
        app.setStyleSheet(ottieni_stylesheet())

def ottieni_stylesheet():
    """Ritorna la stringa QSS basata sulle variabili correnti."""
    return f"""
        /* Widget Generali */
        QWidget {{
            background-color: {IMPOSTAZIONI_STILE["background_color"]};
            color: {IMPOSTAZIONI_STILE["text_color"]};
            font-family: "{IMPOSTAZIONI_STILE["font_family"]}";
            font-size: {IMPOSTAZIONI_STILE["font_size"]}pt;
        }}
        
        /* Contenitore e Gruppi */
        QGroupBox {{
            border: 2px solid {IMPOSTAZIONI_STILE["border_color"]};
            border-radius: 6px;
            margin-top: 12px;
            font-weight: bold;
            padding: 10px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }}

        /* Pulsanti */
        QPushButton {{
            background-color: {IMPOSTAZIONI_STILE["primary_color"]};
            color: {IMPOSTAZIONI_STILE["primary_text"]};
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 4px;
            padding: 6px 12px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: rgba(52, 152, 219, 0.85); /* Leggera trasparenza all'hover */
        }}
        QPushButton:pressed {{
            background-color: rgba(52, 152, 219, 0.7);
        }}
        
        /* Campi di input */
        QLineEdit, QTextEdit, QComboBox, QSpinBox {{
            background-color: #ffffff;
            color: #2c3e50;
            border: 1px solid {IMPOSTAZIONI_STILE["border_color"]};
            border-radius: 4px;
            padding: 5px;
        }}
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
            border: 1.5px solid {IMPOSTAZIONI_STILE["primary_color"]};
        }}

        /* Schede (Tabs) */
        QTabWidget::pane {{
            border: 1px solid {IMPOSTAZIONI_STILE["border_color"]};
            background-color: {IMPOSTAZIONI_STILE["background_color"]};
            border-radius: 4px;
        }}
        QTabBar::tab {{
            background-color: {IMPOSTAZIONI_STILE["secondary_color"]};
            border: 1px solid {IMPOSTAZIONI_STILE["border_color"]};
            border-bottom-color: transparent;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            padding: 8px 16px;
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background-color: {IMPOSTAZIONI_STILE["background_color"]};
            border-bottom-color: transparent;
        }}
        QTabBar::tab:hover {{
            background-color: #e5e9ea;
        }}

        /* Liste e Tabelle */
        QListWidget, QTableWidget {{
            background-color: #ffffff;
            border: 1px solid {IMPOSTAZIONI_STILE["border_color"]};
            border-radius: 4px;
            gridline-color: {IMPOSTAZIONI_STILE["secondary_color"]};
        }}
        QListWidget::item, QTableWidget::item {{
            padding: 6px;
            border-bottom: 1px solid {IMPOSTAZIONI_STILE["secondary_color"]};
        }}
        QListWidget::item:selected, QTableWidget::item:selected {{
            background-color: {IMPOSTAZIONI_STILE["primary_color"]};
            color: {IMPOSTAZIONI_STILE["primary_text"]};
        }}
        
        /* Intestazioni delle tabelle */
        QHeaderView::section {{
            background-color: {IMPOSTAZIONI_STILE["secondary_color"]};
            padding: 4px;
            border: 1px solid {IMPOSTAZIONI_STILE["border_color"]};
            font-weight: bold;
        }}
    """
