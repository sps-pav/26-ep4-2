# Lovec mincí – plán projektu

## Cíl

Vytvořit jednoduchou 2D hru propojenou s databází a webovou prezentací. Postupovat po malých krocích a rozumět každé části kódu.

## Jak hra funguje

- Hráč ovládá čtvereček šipkami.
- Na obrazovce je jedna mince znázorněná žlutým kolečkem.
- Po dotyku s mincí získá hráč bod a mince se objeví na jiném místě.
- Hra trvá 30 sekund. Potom zobrazí a uloží výsledek.
- Menu obsahuje tlačítka Hrát a Konec.
- Hráč je identifikovaný, aby se výsledky ukládaly ke správnému účtu.
- Za dosažení 5, 10 a 20 bodů může získat odznaky.

## Technologie

- Hra: Python + Pygame.
- Web: HTML + CSS + PHP.
- Databáze: MySQL nebo MariaDB.
- Verzování: Git a repozitář od učitele.

Použít technologie probírané ve výuce a ověřit spuštění na školních počítačích ve VT6. Podle zadání slouží AI k inspiraci a textům, nikoliv ke generování celých bloků kódu.

## Postup krok za krokem

### 1. Základ projektu

- [ ] Sepsat krátký popis hry podle části „Jak hra funguje“.
- [ ] Připojit se do repozitáře od učitele.
- [ ] Vytvořit složky `hra`, `web`, `databaze`, `dokumentace`.
- [ ] Ověřit Python a Pygame otevřením prázdného okna.
- [ ] Vytvořit menu s tlačítky Hrát a Konec.
- [ ] Tlačítkem Hrát otevřít zatím prázdnou herní plochu.
- [ ] Tlačítkem Konec zavřít program.

**První pracovní cíl:** funkční okno a menu. Mince a databázi přidávat až potom.

### 2. Návrh databáze a propojení

- [ ] Navrhnout čtyři tabulky podle přehledu níže.
- [ ] Zakreslit ER diagram s vazbami 1:N a M:N.
- [ ] Sepsat datové toky: hra ukládá výsledky do DB; web čte výsledky z DB; registrace na webu vytváří uživatele.
- [ ] Určit, jak hra rozpozná uživatele a přiřadí mu výsledek.

| Tabulka | Účel | Návrh hlavních údajů |
| --- | --- | --- |
| Uživatelé | Herní účty | ID, jedinečné jméno, hash hesla |
| Výsledky | Odehrané hry | ID, ID uživatele, skóre, datum |
| Odznaky | Dostupné odměny | ID, název, potřebný počet bodů |
| Odznaky uživatelů | Propojení hráčů a odznaků | ID uživatele, ID odznaku, datum získání |

Jeden uživatel má více výsledků (1:N). Více uživatelů může získat více odznaků (M:N), proto existuje spojovací tabulka. Stejnou dvojici uživatel–odznak ukládat pouze jednou.

### 3. Základ webu

- [ ] Vytvořit alespoň čtyři HTML stránky: Úvod, Pravidla, Výsledky, O autorovi.
- [ ] Propojit stránky společnou navigací.
- [ ] Použít jeden společný CSS soubor.
- [ ] Připravit místo pro screenshoty a vývojové diagramy.
- [ ] Připravit přihlášení a registraci; funkční propojení doplnit později.

### 4. Herní mechanika

- [ ] Nakreslit čtvereček hráče.
- [ ] Přidat pohyb šipkami a zabránit opuštění herní plochy.
- [ ] Nakreslit jednu minci.
- [ ] Kontrolovat dotyk hráče s mincí.
- [ ] Za sebrání přičíst jeden bod a přesunout minci na náhodné místo v herní ploše.
- [ ] Zobrazovat skóre.
- [ ] Přidat časový limit 30 sekund.
- [ ] Po vypršení času zastavit hru a ukázat výsledek.
- [ ] Umožnit návrat do menu.

### 5. Databáze a propojení

- [ ] Vytvořit SQL skripty CREATE TABLE s datovými typy a potřebnými PK, FK, UNIQUE, NOT NULL, AUTO_INCREMENT a DEFAULT.
- [ ] Vložit alespoň tři vzorové záznamy do každé tabulky.
- [ ] Ověřit návrh databáze podle BCNF.
- [ ] Doplnit identifikaci hráče ve hře.
- [ ] Ukládat výsledky hry do databáze.
- [ ] Zprovoznit registraci a přihlášení na webu; ukládat hash hesla.
- [ ] Zobrazovat na webu výsledky načtené z DB.
- [ ] Přidělovat dosažené odznaky bez duplicit.
- [ ] Používat připravené parametrizované dotazy.
- [ ] Doplnit SELECT s JOIN, WHERE, ORDER BY, GROUP BY a LIKE.
- [ ] Doplnit UPDATE a DELETE, například pro úpravu názvu odznaku a smazání vybraného zkušebního výsledku.
- [ ] Ošetřit chybné vstupy a nedostupnou databázi, aby aplikace nespadla.

### 6. Testy a dokumentace

- [ ] Automatizovaný test: sebrání mince zvýší skóre právě o jeden bod.
- [ ] Automatizovaný test: odznak se přidělí při dosažení hranice, pod hranicí nikoliv.
- [ ] Ověřit, že oba testy jdou spustit a procházejí.
- [ ] Připravit tři vývojové diagramy: sbírání mince, ukončení hry a uložení výsledku, přidělení odznaku.
- [ ] Přidat komentáře ke všem blokům, funkcím a případným třídám.
- [ ] Vytvořit samostatný soubor `dokumentace.md`: účel, technologie, struktura, spuštění, závislosti a omezení.
- [ ] Vytvořit samostatný soubor `manual.md`: spuštění, ovládání, příklady použití a chybové stavy.
- [ ] Vytvořit samostatný soubor `prezentace.md`: problém, řešení, cílová skupina, přínos, ukázka a možnosti rozvoje.
- [ ] Vytvořit samostatný soubor `prehled.md`: struktura kódu, datové toky, technologie, začátek vývoje a rizika.

### 7. Odevzdání

- [ ] Ověřit celé propojení hry, databáze a webu.
- [ ] Vyzkoušet projekt na školním PC ve VT6.
- [ ] Přiložit SQL skripty, ER diagram, diagramy a dokumentaci.
- [ ] Průběžně commitovat: alespoň pět popisných commitů za každou fázi.
- [ ] Zapracovat připomínky učitele.
- [ ] Zkontrolovat, že vše je v repozitáři a učitel k němu má přístup.

## Kontrolní termíny podle zadání

| Termín | Co má být připravené |
| --- | --- |
| Začátek října | Téma, funkční menu, návrh datových toků, návrh databáze a ER diagram |
| Konec listopadu | Pohyb a logika hry, práce s DB a propojení DB s hrou a webem |
| Konec prosince | Kompletní funkční projekt včetně testů a dokumentace |

Pokud některá část první kontroly chybí, dokončit ji jako první. Pak pokračovat herní mechanikou a propojením.

## Pravidlo práce

Vždy dokončit a vyzkoušet jeden malý krok. Teprve potom přidávat další funkci. Základní hra nepotřebuje nepřátele, levely ani složitou grafiku.
