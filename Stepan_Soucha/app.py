from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Tohle bude hlavní stránka e-shopu"

@app.route('/katalog')
def katalog():
    return "Tady bude výpis TCG karet a příslušenství"

@app.route('/kosik')
def kosik():
    return "Zde bude nákupní košík"

@app.route('/profil')
def profil():
    return "Tady bude přihlášení a profil uživatele"

if __name__ == '__main__':
    app.run(debug=True)