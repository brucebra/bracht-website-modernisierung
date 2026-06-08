/**
 * main.js - Menü-Aktivierungs-Logik für die 3-Ebenen-Struktur
 * 
 * Logik:
 * 1. Beim Laden der Seite: Aktuelle URL parsen
 * 2. Aus zuordnung.csv den Menü-Code auslesen (z.B. p_4_2)
 * 3. Alle relevanten Buttons ROT aktivieren (.active-Klasse)
 * 4. Sub- und SubSub-Menüs sichtbar machen
 */

document.addEventListener('DOMContentLoaded', function() {
    // 1. Aktuelle Datei aus URL ermitteln
    const path = window.location.pathname;
    const filename = path.substring(path.lastIndexOf('/') + 1) || 'index.html';
    const currentFile = filename.toLowerCase().replace('.html', '').replace('.htm', '').trim();
    
    // 2. Menü-Daten aus globalem Objekt (wird vom Converter ins HTML geschrieben)
    if (typeof MENU_DATA === 'undefined') {
        console.warn('MENU_DATA nicht gefunden - verwende Fallback');
        activateMenuByFilename(currentFile);
        return;
    }
    
    const menuCode = MENU_DATA[currentFile];
    if (!menuCode) {
        console.warn('Kein Menü-Code für', currentFile);
        return;
    }
    
    // 3. Menü-Code parsen (z.B. "p_4_2" -> ["p", "4", "2"])
    const parts = menuCode.split('_');
    const mainLevel = parts[0];      // z.B. "p"
    const subLevel = parts[1];       // z.B. "4"
    const subsubLevel = parts[2];    // z.B. "2"
    
    // 4. Hauptmenü aktivieren
    const mainBtn = document.getElementById('btn_' + mainLevel);
    if (mainBtn) mainBtn.classList.add('active');
    
    // 5. Sub-Menü anzeigen und aktivieren
    const subMenu = document.getElementById('sub-menu');
    if (subMenu) {
        subMenu.classList.remove('hidden');
        const subBtn = document.querySelector(`[data-sub="${mainLevel}_${subLevel}"]`);
        if (subBtn) subBtn.classList.add('active');
    }
    
    // 6. SubSub-Menü anzeigen und aktivieren
    const subsubMenu = document.getElementById('subsub-menu');
    if (subsubMenu && subsubLevel) {
        subsubMenu.classList.remove('hidden');
        const subsubBtn = document.querySelector(`[data-subsub="${mainLevel}_${subLevel}_${subsubLevel}"]`);
        if (subsubBtn) subsubBtn.classList.add('active');
    }
    
    // 7. Bildwechsel beim Hovern über Thumbnails
    const mainImage = document.getElementById('mainShowImage');
    const thumbLinks = document.querySelectorAll('a[data-large]');
    thumbLinks.forEach(link => {
        link.addEventListener('mouseover', function(e) {
            e.preventDefault();
            const newSrc = this.getAttribute('data-large');
            if (newSrc && mainImage) {
                mainImage.src = newSrc;
            }
        });
    });
    
    // 8. Großansicht beim Klick auf Hauptbild
    if (mainImage) {
        mainImage.addEventListener('click', function() {
            oeffneGrossAnsicht(this.src);
        });
    }
});

/**
 * Fallback: Aktiviere Menü basierend auf Dateinamen
 * (Wenn MENU_DATA nicht vorhanden ist)
 */
function activateMenuByFilename(filename) {
    const mainBtn = document.getElementById('btn_p');
    if (mainBtn) mainBtn.classList.add('active');
}

/**
 * Öffnet Großansicht mit Overlay
 */
function oeffneGrossAnsicht(src) {
    const grossSrc = src.includes('_gross.jpg') ? src : src.replace('.jpg', '_gross.jpg');
    
    const overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.85); z-index:1000; display:flex; align-items:center; justify-content:center; cursor:zoom-out;';
    
    const grossesBild = document.createElement('img');
    grossesBild.src = grossSrc;
    grossesBild.style.cssText = 'max-width:90vw; max-height:90vh; border:3px solid white; box-shadow:0 10px 25px rgba(0,0,0,0.5);';
    
    overlay.appendChild(grossesBild);
    document.body.appendChild(overlay);
    
    overlay.onclick = function() {
        overlay.remove();
    };
}

/**
 * Tauscht das Hauptbild (OnMouseOver der Thumbnails)
 */
function tauscheBild(neuesSrc) {
    const mainImg = document.getElementById('mainShowImage');
    if (mainImg) mainImg.src = neuesSrc;
}
