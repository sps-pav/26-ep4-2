import sqlite3

conn = sqlite3.connect('database/eshop.db')
cursor = conn.cursor()

# 1. Vytvoření kategorie
cursor.execute("INSERT INTO kategorie (nazev) VALUES ('Pokémon Karty')")
id_kategorie = cursor.lastrowid # Získáme ID nově vytvořené kategorie pro použití u produktů

# 2. Vložení karet s využitím PokéAPI obrázků
# Pořadí hodnot: nazev, id_kategorie, cena, kusu_skladem, popis, obrazek_url
karty = [
    ('Charizard', id_kategorie, 2500, 5, 'Holo Rare karta z edice Base Set', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png'),
    ('Pikachu', id_kategorie, 350, 12, 'Bleskový Pokémon, Promo edice', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png'),
    ('Gengar', id_kategorie, 800, 2, 'Temný Pokémon, skvělý do balíčku', 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png')
]

cursor.executemany('''
    INSERT INTO produkt (nazev, id_kategorie, cena, kusu_skladem, popis, obrazek_url)
    VALUES (?, ?, ?, ?, ?, ?)
''', karty)

conn.commit()
conn.close()

print("Kategorie i karty byly úspěšně přidány do databáze!")