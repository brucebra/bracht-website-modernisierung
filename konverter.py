#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Konverter für Bracht + Partner Website Modernisierung
Verwandelt alte Rumpfdateien (.htm) in moderne HTML mit CSS-Flexbox

Phase 1: Hausboot.htm Test
Phase 2+: Alle 72 Dateien automatisch
"""

import os
import re
import csv
import sys
from collections import defaultdict

try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
except Exception:
    base_dir = os.getcwd()

OLD_FOLDER = os.path.join(base_dir, "alte_seiten")
CSV_FILE = os.path.join(base_dir, "zuordnung.csv")
MENU_FILE = os.path.join(base_dir, "Menue_Architektur.csv")
TEMPLATE_FILE = os.path.join(base_dir, "template.html")

# ============================================================================
# DATEN-PARSER
# ============================================================================

def load_mapping_from_csv(csv_path):
    """Lädt zuordnung.csv: Dateiname -> Menü-Code (z.B. p_4_2)"""
    mapping = {}
    if not os.path.exists(csv_path):
        print(f"❌ Fehler: CSV-Datei '{csv_path}' nicht gefunden.")
        return mapping
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # Header überspringen
        for row in reader:
            if len(row) >= 2 and row[0].strip() and row[1].strip():
                old_name = row[0].strip().lower()
                kuerzel = row[1].strip()
                mapping[old_name] = kuerzel
    
    return mapping

def extract_content_from_source(html_content):
    """
    Extrahiert aus der alten Rumpfdatei:
    - Projekttitel (aus <p class="Title">)
    - Text (alles in <p class="fliesstext">)
    - Miniaturen (pics/projects/minis/)
    - Hauptbild (showcontainer Bild)
    """
    
    # Projekttitel extrahieren
    title_match = re.search(
        r'<p[^>]*class="Title"[^>]*>(.*?)</p>',
        html_content,
        re.DOTALL | re.IGNORECASE
    )
    
    project_title = ""
    if title_match:
        title_raw = title_match.group(1)
        # <br> durch Leerzeichen ersetzen
        title_raw = re.sub(r'<br\s*/?>', ' ', title_raw, flags=re.IGNORECASE)
        # Alle anderen Tags entfernen
        project_title = re.sub(r'<[^>]+>', '', title_raw).strip()
        # HTML-Entities dekodieren
        project_title = project_title.replace('&uuml;', 'ü')
        project_title = project_title.replace('&auml;', 'ä')
        project_title = project_title.replace('&ouml;', 'ö')
    
    # Text extrahieren
    text_blocks = re.findall(
        r'<p[^>]*class="fliesstext"[^>]*>(.*?)</p>',
        html_content,
        re.DOTALL | re.IGNORECASE
    )
    clean_text = '\n'.join(text_blocks)
    # HTML-Entities dekodieren
    clean_text = clean_text.replace('&uuml;', 'ü')
    clean_text = clean_text.replace('&auml;', 'ä')
    clean_text = clean_text.replace('&ouml;', 'ö')
    clean_text = clean_text.replace('&nbsp;', ' ')
    clean_text = re.sub(r'<br\s*/?>', '\n', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'<[^>]+>', '', clean_text)  # Alle Tags entfernen
    
    # Miniaturen extrahieren
    minis = re.findall(
        r'src="(pics/projects/minis/[^"]+)"',
        html_content,
        re.IGNORECASE
    )
    
    # Hauptbild extrahieren
    main_match = re.search(
        r'id="showcontainer"[^>]*>.*?src="(pics/projects/[^"]+)"',
        html_content,
        re.DOTALL | re.IGNORECASE
    )
    if not main_match:
        main_match = re.search(
            r'<img[^>]*src="(pics/projects/[^"]+)"[^>]*name="show"',
            html_content,
            re.IGNORECASE
        )
    
    main_img = main_match.group(1).strip() if main_match else "pics/grau.jpg"
    
    return project_title, clean_text, minis, main_img

# ============================================================================
# HTML-GENERATOR
# ============================================================================

def build_menu_html(menu_code):
    """
    Baut Sub- und SubSub-Menü basierend auf menu_code (z.B. "p_4_2")
    
    Statische Struktur für Phase 1 - später aus CSV dynamisch
    """
    
    parts = menu_code.split('_')
    main_level = parts[0] if len(parts) > 0 else 'p'
    sub_level = parts[1] if len(parts) > 1 else '0'
    
    # Menü-Struktur (statisch für Phase 1)
    menu_tree = {
        'p': {
            '1': [  # Wohnungsbau
                ('house_hoffmann.html', 'HouseHoffmannBlack.gif', 'HouseHoffmannRed.gif', '1'),
                ('house_aisslinger.html', 'HouseAisslingerBlack.gif', 'HouseAisslingerRed.gif', '2'),
                ('STC17.html', 'STC17Black.gif', 'STC17Red.gif', '3'),
                ('loftcube.html', 'loftcubeBlack.gif', 'loftcubeRed.gif', '4'),
            ],
            '2': [  # Vorfertigung
                ('wellmade.html', 'wellmadeBlack.gif', 'wellmadeRed.gif', '1'),
                ('bridge_prefabrication.html', 'prefabricationBlack.gif', 'prefabricationRed.gif', '2'),
            ],
            '3': [  # Gewerbebauten
                ('steindamm.html', 'SteindammBlack.gif', 'SteindammRed.gif', '1'),
                ('youth_bank.html', 'youthBankBlack.gif', 'youthBankRed.gif', '2'),
            ],
            '4': [  # Sonderbauten
                ('dan_graham.html', 'DanGrahamBlack.gif', 'DanGrahamRed.gif', '1'),
                ('Hausboot.html', 'HausbootBlack.gif', 'HausbootRed.gif', '2'),
                ('eisbahn.html', 'SkatingRinkBlack.gif', 'SkatingRinkRed.gif', '3'),
            ]
        }
    }
    
    sub_buttons_html = ""
    subsub_buttons_html = ""
    
    # Sub-Buttons bauen
    if main_level in menu_tree:
        for sub_key in sorted(menu_tree[main_level].keys()):
            sub_name_map = {
                '1': ('residentialBlack.gif', 'residentialRed.gif', 'Wohnungsbau'),
                '2': ('prefabricationBlack.gif', 'prefabricationRed.gif', 'Vorfertigung'),
                '3': ('commercialBlack.gif', 'commercialRed.gif', 'Gewerbebauten'),
                '4': ('specialBlack.gif', 'specialRed.gif', 'Sonderbauten'),
            }
            
            if sub_key in sub_name_map:
                black_gif, red_gif, sub_name = sub_name_map[sub_key]
                first_url = menu_tree[main_level][sub_key][0][0] if menu_tree[main_level][sub_key] else '#'
                
                sub_buttons_html += f'''                <a href="{first_url}" class="menu-btn" data-sub="{main_level}_{sub_key}">
                    <img src="pics/buttons/{black_gif}" class="img-black" alt="{sub_name}">
                    <img src="pics/buttons/{red_gif}" class="img-red" alt="{sub_name}">
                </a>
'''
    
    # SubSub-Buttons bauen
    if main_level in menu_tree and sub_level in menu_tree[main_level]:
        projects = menu_tree[main_level][sub_level]
        for i, (url, black, red, order) in enumerate(projects):
            subsub_buttons_html += f'''                <a href="{url}" class="menu-btn" data-subsub="{main_level}_{sub_level}_{order}">
                    <img src="pics/buttons/{black}" class="img-black">
                    <img src="pics/buttons/{red}" class="img-red">
                </a>
'''
    
    return sub_buttons_html, subsub_buttons_html

def generate_html(old_filename, menu_code):
    """
    Konvertiert eine alte Rumpfdatei zur modernen HTML
    """
    
    old_path = os.path.join(OLD_FOLDER, old_filename)
    if not os.path.exists(old_path):
        return None, f"Datei nicht gefunden: {old_path}"
    
    # Template laden
    if not os.path.exists(TEMPLATE_FILE):
        return None, f"Template nicht gefunden: {TEMPLATE_FILE}"
    
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Inhalt extrahieren
    with open(old_path, 'r', encoding='iso-8859-1') as f:
        old_content = f.read()
    
    project_title, text, minis, main_img = extract_content_from_source(old_content)
    
    # Menü generieren
    sub_html, subsub_html = build_menu_html(menu_code)
    
    # Thumbnails generieren
    thumbs_html = ""
    for mini in minis:
        # Versuche die _gross Version zu finden
        gross_version = mini.replace('/minis/', '/').replace('.gif', '_gross.jpg').replace('.jpg', '_gross.jpg')
        thumbs_html += f'''                    <a href="#" data-large="{gross_version}" class="mini-thumbnail-link">
                        <img src="{mini}" class="mini-thumbnail" border="0">
                    </a>
'''
    
    # Text in <p>-Tags wrappen
    text_html = ""
    for line in text.split('\n'):
        line = line.strip()
        if line:
            text_html += f'                    <p class="fliesstext">{line}</p>\n'
    
    # Projekttitel HTML
    title_html = ""
    if project_title:
        title_html = f'                <span class="title-text">{project_title}</span>'
    
    # Platzhalter ersetzen
    new_html = template
    new_html = new_html.replace(
        '<!-- PLATZHALTER_SUB_MENU -->',
        sub_html
    )
    new_html = new_html.replace(
        '<!-- PLATZHALTER_SUBSUB_MENU -->',
        subsub_html
    )
    new_html = new_html.replace(
        '<!-- PLATZHALTER_PROJEKT_TITEL -->',
        title_html
    )
    new_html = new_html.replace(
        '<!-- PLATZHALTER_TEXT -->',
        text_html
    )
    new_html = new_html.replace(
        '<!-- PLATZHALTER_THUMBS -->',
        thumbs_html
    )
    new_html = new_html.replace(
        '<!-- PLATZHALTER_HAUPTBILD -->',
        f'<img src="{main_img}" id="mainShowImage" width="372" height="153" border="0">'
    )
    
    # MENU_DATA ins HTML schreiben (für JavaScript)
    filename_without_ext = old_filename.replace('.htm', '').replace('.html', '').lower()
    menu_data_js = f"<script>const MENU_DATA = {{'{filename_without_ext}': '{menu_code}'}};</script>"
    new_html = new_html.replace('</head>', f'{menu_data_js}\n</head>')
    
    return new_html, None

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "="*50)
    print("      ▶ BRACHT WEBSITE KONVERTER - PHASE 1")
    print("="*50 + "\n")
    
    # CSV laden
    mapping = load_mapping_from_csv(CSV_FILE)
    print(f"✓ {len(mapping)} Dateien aus zuordnung.csv geladen")
    
    # alte_seiten Ordner prüfen
    if not os.path.exists(OLD_FOLDER):
        print(f"❌ Ordner '{OLD_FOLDER}' nicht gefunden.")
        print("   Bitte erstelle: alte_seiten/")
        input("\nDrücke ENTER zum Beenden...")
        return
    
    files_in_old = os.listdir(OLD_FOLDER)
    html_files = [f for f in files_in_old if f.lower().endswith(('.htm', '.html'))]
    print(f"✓ {len(html_files)} HTML-Dateien in alte_seiten/ gefunden")
    
    if len(html_files) == 0:
        print("\n❌ Keine HTML-Dateien in alte_seiten/ gefunden!")
        print("   Bitte lege Rumpfdateien dort ab.")
        input("\nDrücke ENTER zum Beenden...")
        return
    
    # Verarbeite jede Datei
    successful = 0
    failed = 0
    
    for filename in html_files:
        search_key = filename.lower().strip()
        menu_code = mapping.get(search_key)
        
        if not menu_code:
            print(f"⚠ {filename}: Kein Eintrag in zuordnung.csv - übersprungen")
            continue
        
        if menu_code.upper() == 'X':
            print(f"⊘ {filename}: Markiert als 'X' (ignorieren) - übersprungen")
            continue
        
        # HTML generieren
        new_html, error = generate_html(filename, menu_code)
        
        if error:
            print(f"❌ {filename}: {error}")
            failed += 1
            continue
        
        # Neue HTML speichern
        new_filename = filename.replace('.htm', '.html').lower()
        new_path = os.path.join(base_dir, new_filename)
        
        try:
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"✓ {filename} → {new_filename} (Code: {menu_code})")
            successful += 1
        except Exception as e:
            print(f"❌ {filename}: Fehler beim Speichern - {e}")
            failed += 1
    
    # Summary
    print("\n" + "="*50)
    print(f"      🏁 FERTIG - {successful} erfolgreich, {failed} fehler")
    print("="*50 + "\n")
    input("Drücke ENTER zum Beenden...")

if __name__ == "__main__":
    main()
