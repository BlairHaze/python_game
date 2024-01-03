from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/')
def homepage():
    return "<h1>Zacznij swoją epicką przygodę!</h1> <em>Hello, World!</em> <strong>Kocham naleśniki i kotki!</strong>"

@app.route('/<name>')
def name(name):
    return f"Witaj {name}!"

@app.route('/admin')
def admin():
    return redirect(url_for("homepage"))

if __name__ == '__main__':
    app.run(debug=True)
