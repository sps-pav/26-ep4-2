-- Povolení kontroly cizích klíčů v SQLite
PRAGMA foreign_keys = ON;

-- 1. Smazání existujících tabulek a pohledů (pro čistý start)
DROP VIEW IF EXISTS v_nejprodavanejsi_karty;
DROP TABLE IF EXISTS wishlist;
DROP TABLE IF EXISTS obsah_decku;
DROP TABLE IF EXISTS polozka_objednavky;
DROP TABLE IF EXISTS herni_deck;
DROP TABLE IF EXISTS objednavka;
DROP TABLE IF EXISTS produkt;
DROP TABLE IF EXISTS kategorie;
DROP TABLE IF EXISTS uzivatel;

-- 2. Vytvoření hlavních tabulek
CREATE TABLE uzivatel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jmeno TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    heslo_hash TEXT NOT NULL,
    role TEXT DEFAULT 'zakaznik',
    datum_registrace DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE kategorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev TEXT NOT NULL
);

CREATE TABLE produkt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev TEXT NOT NULL,
    id_kategorie INTEGER NOT NULL,
    cena REAL NOT NULL,
    kusu_skladem INTEGER DEFAULT 0,
    popis TEXT,
    FOREIGN KEY (id_kategorie) REFERENCES kategorie(id) ON DELETE RESTRICT
);

CREATE TABLE objednavka (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_uzivatele INTEGER NOT NULL,
    celkova_cena REAL NOT NULL,
    stav TEXT DEFAULT 'nova',
    datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_uzivatele) REFERENCES uzivatel(id) ON DELETE CASCADE
);

CREATE TABLE herni_deck (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev TEXT NOT NULL,
    obtiznost TEXT,
    popis TEXT
);

-- 3. Vytvoření vazebních tabulek (včetně dvou M:N vazeb)
CREATE TABLE polozka_objednavky (
    id_objednavky INTEGER NOT NULL,
    id_produktu INTEGER NOT NULL,
    mnozstvi INTEGER NOT NULL,
    cena_v_dobe_nakupu REAL NOT NULL,
    PRIMARY KEY (id_objednavky, id_produktu),
    FOREIGN KEY (id_objednavky) REFERENCES objednavka(id) ON DELETE CASCADE,
    FOREIGN KEY (id_produktu) REFERENCES produkt(id) ON DELETE RESTRICT
);

-- První M:N vazba (Herní deck ↔ Produkt)
CREATE TABLE obsah_decku (
    id_decku INTEGER NOT NULL,
    id_produktu INTEGER NOT NULL,
    pocet_kopii INTEGER DEFAULT 1,
    PRIMARY KEY (id_decku, id_produktu),
    FOREIGN KEY (id_decku) REFERENCES herni_deck(id) ON DELETE CASCADE,
    FOREIGN KEY (id_produktu) REFERENCES produkt(id) ON DELETE CASCADE
);

-- Druhá M:N vazba (Uživatel ↔ Produkt)
CREATE TABLE wishlist (
    id_uzivatele INTEGER NOT NULL,
    id_produktu INTEGER NOT NULL,
    datum_pridani DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_uzivatele, id_produktu),
    FOREIGN KEY (id_uzivatele) REFERENCES uzivatel(id) ON DELETE CASCADE,
    FOREIGN KEY (id_produktu) REFERENCES produkt(id) ON DELETE CASCADE
);

-- 4. Vytvoření indexů pro zrychlení databáze
CREATE INDEX idx_produkt_nazev ON produkt(nazev);
CREATE INDEX idx_objednavka_uzivatel ON objednavka(id_uzivatele);

-- 5. Vytvoření pohledu (View)
CREATE VIEW v_nejprodavanejsi_karty AS
SELECT 
    p.id, 
    p.nazev, 
    SUM(po.mnozstvi) as celkem_prodano
FROM produkt p
JOIN polozka_objednavky po ON p.id = po.id_produktu
GROUP BY p.id
ORDER BY celkem_prodano DESC;