from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)