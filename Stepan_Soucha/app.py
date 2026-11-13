import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/katalog')
def katalog():
    # 1. Připojení k databázi
    conn = sqlite3.connect('database/eshop.db')
    # Nastavení, aby se z databáze vracely slovníky (můžeme pak psát karta['nazev'])
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    # 2. Vytažení všech produktů
    cursor.execute('SELECT * FROM produkt')
    vsechny_karty = cursor.fetchall()
    conn.close()
    
    # 3. Odeslání dat do HTML šablony
    return render_template('katalog.html', karty=vsechny_karty)

@app.route('/kosik')
def kosik():
    return render_template('kosik.html')

@app.route('/profil')
def profil():
    return render_template('profil.html')

if __name__ == '__main__':
    app.run(debug=True)