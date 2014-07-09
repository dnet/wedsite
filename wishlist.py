#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from contextlib import closing
from base64 import b64decode
import sqlite3, re

def main():
    print 'Ajándék;Leírás;Link;Foglalta'
    with closing(sqlite3.connect('wishlist.sqlite3')) as db:
        cur = db.cursor()
        cur.execute('SELECT label, desc, link, booked FROM wishlist WHERE booked IS NOT NULL')
        for label, desc, link, booked in cur.fetchall():
            print u'{};{};{};{}'.format(label, desc, link,
                    b64decode(booked).decode('utf-8')).encode('utf-8')

if __name__ == '__main__':
    main()
