-- =========================================================================
-- GRAND LINE EMPORIUM - SQL DDL & DML Scripts (Varianta B: E-shop)
-- Autor: Roman Shtefan (SPŠ)
-- =========================================================================

CREATE DATABASE IF NOT EXISTS onepiece_eshop CHARACTER SET utf8mb4 COLLATE utf8mb4_czech_ci;
USE onepiece_eshop;

-- 1. Tabulka: role
CREATE TABLE role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Tabulka: uzivatel
CREATE TABLE uzivatel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jmeno VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    heslo_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id) ON DELETE RESTRICT
);

-- 3. Tabulka: kategorie
CREATE TABLE kategorie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(100) NOT NULL UNIQUE
);

-- 4. Tabulka: produkt
CREATE TABLE produkt (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kategorie_id INT NOT NULL,
    nazev VARCHAR(150) NOT NULL,
    cena_czk DECIMAL(10,2) NOT NULL CHECK (cena_czk >= 0),
    cena_belly BIGINT NOT NULL CHECK (cena_belly >= 0),
    sklad INT NOT NULL DEFAULT 0 CHECK (sklad >= 0),
    FOREIGN KEY (kategorie_id) REFERENCES kategorie(id) ON DELETE CASCADE
);

-- 5. Tabulka: stav_objednavky
CREATE TABLE stav_objednavky (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(50) NOT NULL UNIQUE
);

-- 6. Tabulka: objednavka
CREATE TABLE objednavka (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uzivatel_id INT NOT NULL,
    stav_id INT NOT NULL,
    datum DATETIME DEFAULT CURRENT_TIMESTAMP,
    celkova_cena DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (uzivatel_id) REFERENCES uzivatel(id) ON DELETE RESTRICT,
    FOREIGN KEY (stav_id) REFERENCES stav_objednavky(id) ON DELETE RESTRICT
);

-- 7. Tabulka: polozka_objednavky (Vazební tabulka M:N s vlastními atributy)
CREATE TABLE polozka_objednavky (
    id INT AUTO_INCREMENT PRIMARY KEY,
    objednavka_id INT NOT NULL,
    produkt_id INT NOT NULL,
    mnozstvi INT NOT NULL CHECK (mnozstvi > 0),
    cena_za_kus DECIMAL(10,2) NOT NULL, -- Historie ceny v okamžiku nákupu
    FOREIGN KEY (objednavka_id) REFERENCES objednavka(id) ON DELETE CASCADE,
    FOREIGN KEY (produkt_id) REFERENCES produkt(id) ON DELETE RESTRICT
);

-- =========================================================================
-- VZOROVÁ DATA (INSERT - min. 3 záznamy do každé tabulky)
-- =========================================================================

INSERT INTO role (nazev) VALUES ('Admin'), ('Zákazník'), ('Moderátor');

INSERT INTO uzivatel (jmeno, email, heslo_hash, role_id) VALUES 
('Luffy', 'luffy@strawhats.pirate', '$2y$10$e8...hash1', 2),
('Zoro', 'zoro@swordsman.pirate', '$2y$10$e8...hash2', 2),
('Roman Shtefan', 'admin@grandline.cz', '$2y$10$e8...hash3', 1);

INSERT INTO kategorie (nazev) VALUES ('Figurky'), ('Artefakty a Zbraně'), ('Oblečení');

INSERT INTO produkt (kategorie_id, nazev, cena_czk, cena_belly, sklad) VALUES 
(1, 'Luffy Gear 5 Sun God Nika', 1899.00, 3000000000, 15),
(1, 'Zoro Three-Sword Style', 1699.00, 1111000000, 8),
(2, 'Mera Mera no Mi (Flame Fruit)', 1299.00, 500000000, 5),
(2, 'Replika meče Enma', 2799.00, 1500000000, 3),
(3, 'Luffy Iconic Straw Hat', 499.00, 100000, 25),
(3, 'Jolly Roger Premium Hoodie', 999.00, 300000, 12);

INSERT INTO stav_objednavky (nazev) VALUES ('Nová'), ('Zaplacená'), ('Odeslaná'), ('Zrušená');

INSERT INTO objednavka (uzivatel_id, stav_id, celkova_cena) VALUES 
(1, 1, 3198.00),
(2, 2, 2799.00),
(1, 3, 499.00);

INSERT INTO polozka_objednavky (objednavka_id, produkt_id, mnozstvi, cena_za_kus) VALUES 
(1, 1, 1, 1899.00),
(1, 3, 1, 1299.00),
(2, 4, 1, 2799.00),
(3, 5, 1, 499.00);

-- =========================================================================
-- POHLED (VIEW) A INDEX
-- =========================================================================

-- Pohled na přehled objednávek s jménem uživatele a stavem
CREATE VIEW v_prehled_objednavek AS
O.id AS ObjednavkaID,
U.jmeno AS ZaznamUzivatele,
S.nazev AS StavObjednavky,
O.celkova_cena,
O.datum
FROM objednavka O
JOIN uzivatel U ON O.uzivatel_id = U.id
JOIN stav_objednavky S ON O.stav_id = S.id;

-- Vlastní index pro zrychlení vyhledávání produktů podle názvu
CREATE INDEX idx_produkt_nazev ON produkt(nazev);