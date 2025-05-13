# Konsolenanwendung zum Suchen von Filmen in der Sakila-Datenbank

## 📌 Projektbeschreibung
Konsolenanwendung zum Suchen nach Filmen in der **Sakila**-Datenbank.
Das Projekt ermöglicht es Benutzern, Filme nach Schlüsselwörtern, Genres und Erscheinungsjahr zu finden.
Darüber hinaus speichert die Anwendung Suchanfragen und bietet die Möglichkeit, die beliebtesten Suchanfragen anzuzeigen.

## 🎯 Projektziel
- Implementieren Sie ein praktisches Tool zum Suchen von Filmen in der **Sakila**-Datenbank.
- Ermöglicht Benutzern, Filme nach Stichworten zu finden (10+ Ergebnisse).
- Filtern Sie Filme nach Genre und Jahr (10+ Ergebnisse).
- Zeigen Sie eine Liste der am häufigsten gestellten Fragen an.

## 🛠 Installieren der Datenbank

### 1️⃣ Installieren des MySQL-Servers
Stellen Sie eine Verbindung zur **Sakila**-Datenbank her.
use sakila; 

### 2️⃣  Einrichten der Konfiguration
Erstellen Sie eine .env- oder config.py-Datei mit Ihren Datenbankverbindungsparametern:

python
CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ваш_пароль',
    'database': 'sakila'
}

Endgültige Struktur des Projekts:
movie_app/
├── main.py             # Einstiegspunkt, Startmenü
├── db.py               # Arbeiten mit der Datenbank, Verbindung, Initialisierung, Speichern von Abfragen
├── models.py           # Datenmodelle
├── search.py           # Suchlogik, Ausgabe, Arbeiten mit Abfragen
├── utils.py            # schöner Abschluss
├── menu.py             # Hauptmenü
├── menu_search.py      # Zusatzmenü
└── valid_years.py      # Gültigkeit des Jahres

### 🚀 Verfügbare Befehle
Die Anwendung funktioniert interaktiv über die Konsole..

Grundlegende Befehle:
Suche nach Filmtitel


Stichwort eingeben: 
Ausgabe: Liste der gefundenen Filme.

Suche nach Genre


Geben Sie den Genrenamen ein:
Fazit: Liste von Filmen dieses Genres.

Suche nach Jahr


Jahr eingeben: 2020
Fazit: Im angegebenen Jahr erschienene Filme.

Beliebte Suchanfragen anzeigen

Wählen Sie den Menüpunkt: 3
Fazit: Die häufigsten Anfragen.

Beenden des Programms

Wählen Sie den Menüpunkt: 0

### 📌 Anwendungsbeispiel

$ python main.py

Anfragenummer auswählen:
1. Suche nach Namensteil (10+ Ergebnisse)
2. Suche nach Genre (10+ Ergebnisse)
3. Beliebte Suchanfragen anzeigen
0. Ausfahrt

> Stichwort eingeben: "Ava"
Abschluss:

Filme, die mit dem Schlüsselwort übereinstimmen 'Ava':
╒═════╤═══════════════╤════════════════╤════════════╤══════════╤═══════════════╤══════════╤══════════════════════╤════════════════════════════════╕
│  #  │     Title     │Erscheinungsjahr│  Kategorie │  Länge   │  Mietpreis    │Bewertung │Bewertungsbeschreibung│          Beschreibung          │
╞═════╪═══════════════╪════════════════╪════════════╪══════════╪═══════════════╪══════════╪══════════════════════╪════════════════════════════════╡
│  1  │ SAVANNAH TOWN │      1998      │   Drama    │    84    │     0.99      │  PG-13   │   Parents Strongly   │   A Awe-Inspiring Tale of a    │
│     │               │                │            │          │               │          │      Cautioned       │    Astronaut And a Database    │
│     │               │                │            │          │               │          │                      │ Administrator who must Chase a │
│     │               │                │            │          │               │          │                      │  Secret Agent in The Gulf of   │
│     │               │                │            │          │               │          │                      │             Mexico             │
├─────┼───────────────┼────────────────┼────────────┼──────────┼───────────────┼──────────┼──────────────────────┼────────────────────────────────┤
│  2  │   ANYTHING    │      1999      │   Horror   │    82    │     2.99      │    R     │      Restricted      │ A Epic Story of a Pastry Chef  │
│     │   SAVANNAH    │                │            │          │               │          │                      │  And a Woman who must Chase a  │
│     │               │                │            │          │               │          │                      │  Feminist in An Abandoned Fun  │
│     │               │                │            │          │               │          │                      │             House              │
├─────┼───────────────┼────────────────┼────────────┼──────────┼───────────────┼──────────┼──────────────────────┼────────────────────────────────┤
│  3  │ KICK SAVANNAH │      1992      │   Travel   │   179    │     0.99      │  PG-13   │   Parents Strongly   │ A Emotional Drama of a Monkey  │
│     │               │                │            │          │               │          │      Cautioned       │ And a Robot who must Defeat a  │
│     │               │                │            │          │               │          │                      │     Monkey in New Orleans      │

🏆 Abklemmung
Dieses Projekt bietet ein einzigartiges Instrument zur Aufnahme von Filmen auf der Basis von Sakila. Verwenden Sie die Anwendung zum Erstellen von Fotos, 
zum Analysieren von Filmen und zum Herunterladen von Filmen.

🎬 Persönliche Beratung!

:)
