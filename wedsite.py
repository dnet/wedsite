#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request
from contextlib import closing
from base64 import b64encode
import sqlite3, re

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

# CREATE TABLE wishlist (id INTEGER PRIMARY KEY AUTOINCREMENT, label, desc, link, booked, changed);
@app.route('/naszajandek.html', methods=['GET', 'POST'])
def wishlist():
    name = request.form.get('name', '')
    checked = [int(key) for key in request.form.iterkeys() if re.match(r'^\d+$', key)]
    msg = None
    success = False
    with closing(sqlite3.connect('wishlist.sqlite3')) as db:
        cur = db.cursor()
        with db:
            if request.method == 'POST':
                if not name:
                    msg = u'Kérlek add meg a nevedet!'
                elif not checked:
                    msg = u'Kérlek jelölj meg legalább egy ajándékot!'
                else:
                    msg = u'Sikeresen lefoglaltad a kiválasztott ajándéko{0}t, köszönjük!'.format(
                            '' if len(checked) == 1 else 'ka')
                    cur.executemany('''UPDATE wishlist SET booked = ?, changed = CURRENT_TIMESTAMP
                            WHERE id = ? AND booked IS NULL''',
                            ((b64encode(name.encode('utf-8')), item) for item in checked))
                    success = True
            items = cur.execute('SELECT id, label, IFNULL(desc, ""), link, booked FROM wishlist').fetchall()
    return render_template('wishlist.html', wishlist=True, items=items,
            name=name, checked=checked, msg=msg, success=success)

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
