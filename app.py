from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/<name>')
def homepage(name):
    return render_template("index.html", content=name, r = 15)
#"<h1>Zacznij swoją epicką przygodę!</h1> <em>Hello, World!</em> <strong>Kocham naleśniki i kotki!</strong>"

@app.route('/<name>')
def name(name):
    return f"Witaj {name}!"

@app.route('/admin')
def admin():
    return redirect(url_for("homepage"))

if __name__ == '__main__':
    app.run(debug=True)
