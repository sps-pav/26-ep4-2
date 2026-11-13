from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/katalog')
def katalog():
    return render_template('katalog.html')

@app.route('/kosik')
def kosik():
    return render_template('kosik.html')

@app.route('/profil')
def profil():
    return render_template('profil.html')

if __name__ == '__main__':
    app.run(debug=True)