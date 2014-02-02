#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', home=True)

@app.route('/egyhazi.html')
def egyhazi():
    return render_template('egyhazi.html', egyhazi=True)

@app.route('/polgari.html')
def polgari():
    return render_template('polgari.html', polgari=True)

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
