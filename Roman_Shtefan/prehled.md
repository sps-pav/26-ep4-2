# Přehled struktury kódu a technických toků

## 1. Struktura JavaScript kódu v `index.html`
Kód je rozdělen do logických modulů a funkcí:
* `products` (Pole objektů): Datová základna obsahující ID, kategorii, ikonu/obrazek, název, cenu v CZK a cenu v Belly.
* `renderProducts(items)`: Generuje HTML strukturu karet produktů do DOM stromu na základě filtrovaných dat.
* `filterProducts()`: Zpracovává vstup z vyhledávacího pole i selectu kategorií a provádí okamžitý real-time filtrační dotaz.
* `addToCart(id)` / `changeQuantity(id, delta)` / `removeFromCart(id)`: Správa stavu nákupního košíku.
* `saveAndUpdateCart()`: Zajišťuje persistenci dat pomocí `localStorage.setItem` a aktualizuje uživatelské rozhraní.

## 2. Datové toky (Data Flow)
1. Uživatel zadá text do vyhledávání nebo zvolí kategorii -> Spustí se `filterProducts()`.
2. Aplikace prohledá pole produktů -> Vykreslí se odpovídající položky přes `renderProducts()`.
3. Uživatel klikne na „Přidat do košíku“ -> Objekt se přidá do proměnné `cart` -> Uloží se do `localStorage` -> Aktualizuje se počítadlo v hlavičce.