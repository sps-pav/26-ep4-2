# Dokumentace projektu – Grand Line Emporium (One Piece E-shop)

**Autor:** Roman Shtefan  
**Třída:** EP4 (26-ep4-2)  
**Škola:** SPŠ  
**Téma:** E-shop s merchandise a sběratelskými předměty One Piece  

## 1. Účel a cíl projektu
Cílem projektu je vytvořit plně funkční, vizuálně přitažlivý a responzivní e-shop zaměřený na fanoušky anime One Piece. Projekt slouží jako samostatná maturitní práce (Varianta B – E-shop) a propojuje moderní frontendové technologie se strukturou relační databáze.

## 2. Použité technologie
* **Frontend:** HTML5, CSS3 (Custom Properties, Flexbox, Grid), JavaScript (Vanilla ES6+, localStorage API)
* **Správa dat:** Lokální úložiště prohlížeče (localStorage) / Návrh relační SQL databáze (MySQL/MariaDB/SQLite)
* **Verzování:** Git, GitHub (`sps-pav/26-ep4-2/Roman_Shtefan`)

## 3. Architektura a struktura projektu
Projekt je navržen jako jednostránková webová aplikace (SPA/PWA princip) s dynamickým vykreslováním katalogu, živým vyhledáváním, filtrováním podle kategorií a plně interaktivním nákupním košíkem.
## 4. Návrh databáze (Splnění požadavků BCNF)
Databáze e-shopu je navržena pro minimálně 7 tabulek s vazbami 1:N a M:N:
1. `uzivatel` – zákazníci a administrátoři
2. `role` – uživatelská oprávnění (zákazník / admin)
3. `kategorie` – rozdělení sortimentu (figurky, artefakty, oblečení)
4. `produkt` – zboží v e-shopu (cena v CZK i v Belly ฿, skladové zásoby)
5. `objednávka` – hlavička objednávky uživatele
6. `polozka_objednavky` – vazební tabulka M:N s dodatečnými atributy (množství, cena v okamžiku nákupu)
7. `stav_objednavky` – stavy (Nová, Zaplacená, Odeslaná, Zrušená)

Všechny tabulky splňují 3. normální formu (3NF) až Boyceho-Coddovu normální formu (BCNF) – každý neklíčový atribut závisí plně na primárním klíči.