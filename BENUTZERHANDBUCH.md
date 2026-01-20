# Datei_M Benutzerhandbuch

## Inhaltsverzeichnis
1. [Einführung](#einführung)
2. [Installation](#installation)
3. [Module](#module)
4. [Verwendungsbeispiele](#verwendungsbeispiele)
5. [Tipps und Tricks](#tipps-und-tricks)

## Einführung

Datei_M ist ein Desktop-Tool, das speziell für das effiziente Sortieren, Analysieren und Organisieren von Dateien und Dokumenten entwickelt wurde. Die Anwendung bietet vier spezialisierte Module, die verschiedene Aspekte der Dateiverwaltung abdecken.

### Hauptmerkmale
- **Benutzerfreundliche GUI** basierend auf Tkinter
- **Modular aufgebaut** - jedes Modul kann unabhängig verwendet werden
- **Regelbasiert** - definieren Sie eigene Regeln für die Dokumentenverarbeitung
- **Erweiterbar** - Unterstützung für zukünftige OCR-Integration
- **Plattformübergreifend** - läuft auf Windows, macOS und Linux

## Installation

### Voraussetzungen
- Python 3.8 oder höher
- tkinter (normalerweise in Python enthalten)

### Schritt-für-Schritt Installation

1. **Repository klonen:**
```bash
git clone https://github.com/ensergej-sketch/Datei_M.git
cd Datei_M
```

2. **Abhängigkeiten installieren:**
```bash
pip install -r requirements.txt
```

3. **Anwendung starten:**
```bash
python main.py
```

### Für Windows-Benutzer
Wenn tkinter nicht verfügbar ist:
```bash
# Python über den offiziellen Installer installieren
# und sicherstellen, dass "tcl/tk and IDLE" ausgewählt ist
```

### Für Linux-Benutzer
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## Module

### 1. Dateien Manager 📁

Der Dateien Manager hilft beim automatischen Aufräumen und Organisieren von Ordnern.

**Funktionen:**
- Sortierung nach Dateityp
- Sortierung nach Datum
- Duplikaterkennung
- Vorschau vor dem Aufräumen
- Verschieben oder Kopieren von Dateien

**Verwendung:**
1. Wählen Sie einen Quellordner aus
2. Optional: Wählen Sie einen Zielordner (sonst wird im Quellordner organisiert)
3. Wählen Sie Sortieroptionen
4. Klicken Sie auf "Vorschau anzeigen" um zu sehen, was passieren wird
5. Klicken Sie auf "Aufräumen starten"

**Beispiel:**
- Quellordner: `C:\Users\Max\Downloads`
- Zielordner: `C:\Users\Max\Sortiert`
- Option: Nach Dateityp sortieren
- Ergebnis: Dateien werden in Unterordner wie `PDF/`, `DOCX/`, `JPG/` organisiert

### 2. Dokumente Manager 📄

Intelligente Dokumentenverwaltung mit regelbasierter Verarbeitung.

**Funktionen:**
- Regelbasierte Dokumentenverarbeitung
- Vordefinierte Regeln für Rechnungen, Briefe, Verträge
- Benutzerdefinierte Regeln erstellen
- OCR-Vorbereitung (für zukünftige Integration)
- Automatische Kategorisierung

**Verwendung:**
1. Wählen Sie einen Dokumentenordner
2. Fügen Sie Regeln hinzu (vordefiniert oder benutzerdefiniert)
3. Konfigurieren Sie OCR-Optionen
4. Analysieren Sie Dokumente
5. Starten Sie die Verarbeitung

**Regel-Beispiele:**
- **Rechnung:** Sucht nach "rechnung", "invoice", "betrag", "mwst"
- **Brief:** Sucht nach "sehr geehrte", "mit freundlichen grüßen"
- **Vertrag:** Sucht nach "vertrag", "vereinbarung"

### 3. Regex Editor 🔍

Komfortabler Editor zum Erstellen und Testen von regulären Ausdrücken.

**Funktionen:**
- Visuelle Regex-Erstellung
- Live-Vorschau der Treffer
- Mustervorlagen für häufige Anwendungsfälle
- Highlighting der gefundenen Treffer
- Optionen für Groß-/Kleinschreibung, Multiline, etc.

**Vordefinierte Muster:**
- E-Mail-Adressen
- Telefonnummern (DE)
- Datum (DD.MM.YYYY)
- PLZ (DE)
- IBAN

**Verwendung:**
1. Wählen Sie eine Mustervorlage oder geben Sie ein eigenes Muster ein
2. Geben Sie einen Testtext ein
3. Klicken Sie auf "Muster testen"
4. Sehen Sie die Treffer und deren Position
5. Speichern Sie erfolgreiche Muster

**Beispiel-Workflow:**
```
Muster: \b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b
Testtext: "Kontakt: info@example.de oder support@test.com"
Ergebnis: 2 Treffer gefunden
  - info@example.de
  - support@test.com
```

### 4. Kategorie Manager 🏷️

Trainieren und Verwalten von Kategorien für Textklassifikation.

**Funktionen:**
- Kategorien erstellen und verwalten
- Begriffe zu Kategorien hinzufügen
- Textklassifikation basierend auf Begriffen
- Import/Export von Kategoriedefinitionen (JSON)
- Statistiken anzeigen

**Vordefinierte Kategorien:**
- Rechnung
- Brief
- Vertrag
- Technisch
- Finanzen

**Verwendung:**
1. Erstellen Sie neue Kategorien oder verwenden Sie vordefinierte
2. Fügen Sie Begriffe zu Kategorien hinzu
3. Testen Sie die Klassifikation mit einem Text
4. Exportieren Sie Kategorien für späteren Gebrauch

**Beispiel-Klassifikation:**
```
Text: "Die Rechnung über 150 EUR inklusive MwSt. wird überwiesen."
Ergebnis: Kategorie "Rechnung" (Treffer: rechnung, mwst, betrag)
```

## Verwendungsbeispiele

### Beispiel 1: Download-Ordner aufräumen

```
Problem: 500 Dateien im Download-Ordner durcheinander
Lösung: Dateien Manager verwenden

1. Modul öffnen
2. Quellordner: C:\Users\Name\Downloads
3. Option: Nach Dateityp sortieren aktivieren
4. Vorschau anzeigen
5. Aufräumen starten

Ergebnis: Dateien in Ordnern PDF/, DOCX/, JPG/, etc.
```

### Beispiel 2: Rechnungen automatisch erkennen

```
Problem: Viele PDFs, Rechnungen manuell heraussuchen
Lösung: Dokumente Manager verwenden

1. Modul öffnen
2. Dokumentenordner auswählen
3. Regel "Rechnungen erkennen" hinzufügen
4. Dokumente analysieren
5. Verarbeitung starten

Ergebnis: Rechnungen werden identifiziert und können sortiert werden
```

### Beispiel 3: E-Mail-Adressen aus Text extrahieren

```
Problem: E-Mail-Adressen aus einem Text extrahieren
Lösung: Regex Editor verwenden

1. Modul öffnen
2. Vorlage "E-Mail" auswählen
3. Text einfügen
4. "Muster testen" klicken
5. Alle E-Mail-Adressen werden hervorgehoben

Ergebnis: Liste aller gefundenen E-Mail-Adressen
```

### Beispiel 4: Dokumente kategorisieren

```
Problem: Texte verschiedenen Themen zuordnen
Lösung: Kategorie Manager verwenden

1. Modul öffnen
2. Kategorien definieren (z.B. "Marketing", "Technik", "Finanzen")
3. Begriffe zu jeder Kategorie hinzufügen
4. Text eingeben und klassifizieren
5. Export für spätere Verwendung

Ergebnis: Automatische Kategoriezuordnung basierend auf Begriffen
```

## Tipps und Tricks

### Allgemein
- **Backup erstellen:** Erstellen Sie immer ein Backup, bevor Sie große Organisierungsaktionen durchführen
- **Vorschau nutzen:** Verwenden Sie die Vorschau-Funktion, um Änderungen vor der Ausführung zu prüfen
- **Schrittweise vorgehen:** Testen Sie mit kleinen Ordnern, bevor Sie große Mengen verarbeiten

### Dateien Manager
- **Zielordner:** Lassen Sie das Zielordner-Feld leer, um im Quellordner zu organisieren
- **Duplikate:** Aktivieren Sie "Duplikate entfernen" mit Vorsicht - überprüfen Sie die Vorschau
- **Unterordner:** Aktuell werden nur Dateien im Hauptverzeichnis verarbeitet, nicht in Unterordnern

### Dokumente Manager
- **Regeln kombinieren:** Erstellen Sie mehrere Regeln für verschiedene Dokumenttypen
- **Suchbegriffe:** Verwenden Sie mehrere Begriffe mit "|" getrennt: "rechnung|invoice|bill"
- **Testen:** Analysieren Sie Dokumente zuerst, bevor Sie die Verarbeitung starten

### Regex Editor
- **Einfach starten:** Beginnen Sie mit vordefinierten Mustern und passen Sie diese an
- **Testen:** Testen Sie Ihre Muster mit verschiedenen Beispielen
- **Optionen:** Nutzen Sie IGNORECASE für flexible Suchen
- **Gruppen:** Verwenden Sie Klammern () um Teile zu gruppieren

### Kategorie Manager
- **Begriffe sammeln:** Fügen Sie viele relevante Begriffe zu Kategorien hinzu
- **Synonyme:** Fügen Sie Synonyme und verschiedene Schreibweisen hinzu
- **Export:** Exportieren Sie Ihre Kategorien regelmäßig als Backup
- **Statistik:** Nutzen Sie die Statistik-Funktion, um die Qualität Ihrer Kategorien zu prüfen

## Fehlerbehebung

### Fehler: "tkinter nicht gefunden"
**Lösung:** Installieren Sie tkinter für Ihre Python-Version (siehe Installation)

### Fehler: "Keine Berechtigung zum Verschieben von Dateien"
**Lösung:** Führen Sie die Anwendung mit ausreichenden Rechten aus oder wählen Sie einen Ordner mit Schreibrechten

### Fehler: "Regex-Fehler"
**Lösung:** Überprüfen Sie Ihr Regex-Muster auf Syntaxfehler. Nutzen Sie die vordefinierten Muster als Basis.

## Zukünftige Erweiterungen

Geplante Features für zukünftige Versionen:
- Vollständige OCR-Integration mit Tesseract
- PDF-Textextraktion
- Maschinelles Lernen für Textklassifikation
- Batch-Verarbeitung
- Automatische Dateiumbenennung
- Duplikatsuche basierend auf Inhalt
- Cloud-Integration
- Mehrsprachige Unterstützung

## Support und Beiträge

Bei Fragen oder Problemen:
- Erstellen Sie ein Issue auf GitHub
- Kontaktieren Sie den Autor

Beiträge sind willkommen! Erstellen Sie Pull Requests für:
- Bugfixes
- Neue Features
- Dokumentationsverbesserungen
- Übersetzungen

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe LICENSE-Datei für Details.

---

**Viel Erfolg beim Organisieren Ihrer Dateien mit Datei_M! 📁✨**
