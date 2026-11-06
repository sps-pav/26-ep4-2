import sqlite3
import os

# Nastavení cest k souborům
SCHEMA_PATH = os.path.join('database', 'schema.sql')
DB_PATH = os.path.join('database', 'eshop.db')

def init_db():
    print("Vytvářím databázi...")
    
    # Navázání spojení (pokud soubor eshop.db neexistuje, Python ho sám vytvoří)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Načtení našeho SQL návrhu
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    # Spuštění všech SQL příkazů najednou
    cursor.executescript(sql_script)

    # Uložení změn a bezpečné ukončení
    conn.commit()
    conn.close()

    print("Hotovo! Databáze eshop.db je připravena.")

if __name__ == '__main__':
    init_db()