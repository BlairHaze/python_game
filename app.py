from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! Kocham naleśniki i kotki!'

if __name__ == '__main__':
    app.run(debug=True)