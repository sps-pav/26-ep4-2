# Uživatelský manuál – Grand Line Emporium

## 1. Spuštění aplikace
Pro spuštění e-shopu není nutná instalace žádného serveru ani Node.js:
1. Otevřete složku projektu.
2. Dvakrát klikněte na soubor **`index.html`** nebo jej otevřete ve webovém prohlížeči (Google Chrome, Firefox, Edge).

## 2. Popis uživatelského rozhraní (UI)
* **Hlavička (Header):** Obsahuje logo obchodu, interaktivní **vyhledávací pole** pro okamžité nalezení zboží podle názvu a tlačítko **Košík** s počítadlem položek.
* **Hlavní banner:** Uvítací sekce s tematickým mottem One Piece.
* **Katalog zboží:** Grid mřížka produktů. Každý produkt obsahuje štítek kategorie, název, cenu v českých korunách (CZK) a pirátské měně (Belly ฿).
* **Filtrování:** Rozbalovací seznam pro filtrování podle kategorií (Figurky, Artefakty, Oblečení).

## 3. Práce s nákupním košíkem
1. Kliknutím na tlačítko **„Přidat do košíku“** u vybraného produktu se zboží uloží do košíku.
2. Kliknutím na tlačítko **Košík** v pravém horním rohu se otevře modální okno.
3. V košíku můžete:
   * Množství položek upravovat pomocí tlačítek `+` a `-`.
   * Položku zcela odstranit pomocí tlačítka `✕`.
   * Vidět celkovou kalkulaci ceny v CZK.
4. Data v košíku se automaticky ukládají do paměti prohlížeče (`localStorage`), takže po obnovení stránky o vybrané zboží nepřijdete.
5. Kliknutím na **„Dokončit objednávku“** se simuluje odeslání objednávky a košík se vyprázdní.