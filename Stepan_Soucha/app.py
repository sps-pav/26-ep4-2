import sqlite3
from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
# Tajný klíč je nutný pro bezpečnost Sessions (v reálu by to bylo složité heslo)
app.secret_key = 'tajny_klic_pro_maturitu' 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/katalog')
def katalog():
    # 1. Připojení k databázi
    conn = sqlite3.connect('database/eshop.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    # 2. Vytažení všech produktů
    cursor.execute('SELECT * FROM produkt')
    vsechny_karty = cursor.fetchall()
    conn.close()
    
    # 3. Odeslání dat do HTML šablony
    return render_template('katalog.html', karty=vsechny_karty)

# Nová funkce: Zpracuje kliknutí na tlačítko "Přidat do košíku"
@app.route('/pridat_do_kosiku/<int:id_produktu>', methods=['POST'])
def pridat_do_kosiku(id_produktu):
    # Pokud košík ještě neexistuje, vytvoříme ho jako prázdný seznam
    if 'kosik' not in session:
        session['kosik'] = []
    
    # Přidáme ID karty do košíku a session uložíme
    session['kosik'].append(id_produktu)
    session.modified = True
    
    # Po kliknutí uživatele hned vrátíme zpět do katalogu
    return redirect(url_for('katalog'))

@app.route('/kosik')
def kosik():
    kosik_ids = session.get('kosik', [])
    karty_v_kosiku = []
    celkova_cena = 0
    
    # Pokud v košíku něco je, připojíme se do databáze a vytáhneme detaily
    if kosik_ids:
        conn = sqlite3.connect('database/eshop.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Projdeme všechna uložená ID a načteme k nim data
        for id_produktu in kosik_ids:
            cursor.execute('SELECT * FROM produkt WHERE id = ?', (id_produktu,))
            karta = cursor.fetchone()
            if karta:
                karty_v_kosiku.append(karta)
                celkova_cena += karta['cena']
                
        conn.close()
        
    return render_template('kosik.html', karty=karty_v_kosiku, celkem=celkova_cena)

# Nová funkce pro smazání košíku
@app.route('/vyprazdnit_kosik', methods=['POST'])
def vyprazdnit_kosik():
    session.pop('kosik', None) # Smaže košík z paměti
    return redirect(url_for('kosik'))

@app.route('/profil')
def profil():
    return render_template('profil.html')

if __name__ == '__main__':
    app.run(debug=True)