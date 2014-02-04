#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for, request
from contextlib import closing
import sqlite3

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

@app.route('/kapcsolat.html')
def kapcsolat():
    return render_template('kapcsolat.html', kapcsolat=True)

FIELDS = ('names', 'notes')
EVENTS = ('egyhazi', 'polgari', 'vacsora')

@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    success = False
    if request.method == 'POST':
        rf = request.form
        invalid = not rf.get('names') or not any(event in rf for event in EVENTS)
        if not invalid:
            success = True
            save_rsvp()
    else:
        invalid = False
    return render_template('rsvp.html', invalid=invalid, success=success, fields=request.form)

# CREATE TABLE rsvp (names, egyhazi, polgari, vacsora, notes);
def save_rsvp():
    with closing(sqlite3.connect('rsvp.sqlite3')) as db:
        with db:
            keys = list(FIELDS) + list(EVENTS)
            db.execute('INSERT INTO rsvp ({fields}) VALUES ({qmarks})'.format(
                fields=','.join(keys), qmarks=','.join('?' * len(keys))),
                [request.form.get(key) for key in keys])

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
