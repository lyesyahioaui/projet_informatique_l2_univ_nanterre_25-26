# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras

def connect_to_db():
    conn = psycopg2.connect(
    dbname="nature_db",
    user="lyesyahiaoui",
    password="*Lyes200406#",
    host="localhost",
    port=5432,
    cursor_factory=psycopg2.extras.NamedTupleCursor,
    client_encoding='UTF8'
)

    conn.autocommit = True
    return conn
