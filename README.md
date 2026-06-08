# Bracht + Partner Architekten Website Modernisierung

## Projekt: Von Frames (2006) zu flexiblem CSS-Layout

Modernisierung der Bracht + Partner Architekten Website. Umwandlung von veralteten HTML-Frames in ein modernes, flexibles CSS-Grid-System.

## Phase 1: Hausboot.html Test

### Setup

1. **Struktur aufbauen:**
   ```
   projekt/
   ├── alte_seiten/         ← Rumpfdateien hier ablegen
   ├── css/
   │   └── style.css
   ├── js/
   │   └── main.js
   ├── pics/                ← Bilder (background.jpg, buttons/, projects/)
   ├── template.html        ← Master-Template
   ├── konverter.py         ← Konverter-Skript
   ├── zuordnung.csv        ← Zuordnung Datei → Menü-Code
   └── Menue_Architektur.csv → Menü-Struktur
   ```

2. **Rumpfdatei ablegen:**
   - Lege `Hausboot.htm` in den `alte_seiten/` Ordner

3. **Konverter ausführen:**
   ```bash
   python3 konverter.py
   ```

4. **Output prüfen:**
   - `Hausboot.html` sollte im Root-Verzeichnis erstellt werden
   - Browser öffnen: `file:///pfad/zu/Hausboot.html`

### Was macht der Konverter?

1. Liest alte Rumpfdatei (`Hausboot.htm`) aus `/alte_seiten/`
2. Findet Menü-Code in `zuordnung.csv` (z.B. `Hausboot.htm;p_4_2`)
3. Extrahiert Inhalte:
   - Text (alle `<p class="fliesstext">`)
   - Miniaturen (pics/projects/minis/)
   - Hauptbild
4. Generiert Menü basierend auf Code:
   - `p` = Hauptmenü "Projekte"
   - `4` = Sub "Sonderbauten"
   - `2` = SubSub "Hausboot"
5. Schreibt alles ins `template.html`
6. Speichert als `Hausboot.html`

### CSS-Besonderheiten

- **Alphabetisch sortiert** (A-Z)
- **Nur CSS für Hover** (Black ↔ Red)
- **`.active` Klasse** für permanente Rot-Färbung
- **`.hidden` Klasse** für Sub/SubSub initial versteckt
- **Grid-System** 282px + 116px + 340px (Gesamt: 738px)

### JavaScript-Logik

- Beim Laden: URL parsen (z.B. `Hausboot.html`)
- MENU_DATA aus HTML auslesen
- Alle 3 Menü-Ebenen `.active` setzen
- Sub/SubSub `.hidden` entfernen
- Bildwechsel bei Thumbnail-Hover
- Großansicht beim Klick auf Hauptbild

## Phase 2+: Batch-Processing

Sobald Phase 1 funktioniert:
1. Alle 72 Rumpfdateien in `/alte_seiten/` ablegen
2. `konverter.py` erneut ausführen
3. Alle `.html` Dateien erscheinen im Root

## Problembehebung

### Hausboot.html wird nicht generiert
- ✓ Datei liegt in `alte_seiten/Hausboot.htm`?
- ✓ CSV-Eintrag existiert: `Hausboot.htm;p_4_2`?
- ✓ `template.html` existiert im Root?
- ✓ `konverter.py` hat keine Fehler?

### Bilder fehlen
- ✓ `/pics/` Ordner mit allen Unterordnern vorhanden?
- ✓ Pfade stimmen: `pics/background.jpg`, `pics/buttons/`, `pics/projects/`

### Menü ist falsch
- ✓ CSV-Code korrekt? (Format: `p_4_2`)
- ✓ Buttons in `pics/buttons/` vorhanden?

## Nächste Schritte

1. ✅ Hausboot.htm in `alte_seiten/` ablegen
2. ✅ `konverter.py` ausführen
3. ⏳ Hausboot.html prüfen
4. ⏳ Layout, Menü, Bilder validieren
5. ⏳ Ggf. anpassen
6. ⏳ Alle 72 Dateien durchlaufen

---

**Status:** Phase 1 Setup ✓ | Hausboot Test ⏳ | Batch Processing ⏳
