#!/usr/bin/python3
from urllib.robotparser import RequestRate
from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

import psycopg2
import psycopg2.extras

## SGBD configs
DB_HOST = "db.tecnico.ulisboa.pt"
DB_USER = "ist199088"
DB_DATABASE = DB_USER
DB_PASSWORD = "jackers"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (
    DB_HOST,
    DB_DATABASE,
    DB_USER,
    DB_PASSWORD,
)

app = Flask(__name__)

@app.route("/")
def root():
    try:
        return render_template("root.html")
    except Exception as e:
        return str(e)  # Renders a page with the error.

@app.route("/a")
def a():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT nome FROM categoria;"
        cursor.execute(query)
        return render_template("a.html", cursor=cursor)
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        dbConn.close()

@app.route("/new_cat", methods=["POST"])
def new_cat():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cat_name = request.form["cat_name"]
        cat_type = request.form["cat_type"]
        if(cat_type == "Categoria Simples"):
            query = "INSERT INTO categoria VALUES (%s);b"
        else:
            query = "INSERT INTO categoria VALUES (%s);"
        data = (cat_name, cat_name)
        cursor.execute(query, data)
        return query
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route("/add_sub", methods=["POST"])
def add_sub():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sub_name = request.form["sub_name"]
        super_name = request.form["super_name"]
        print(sub_name + " " + super_name)
        query = "INSERT INTO tem_outra VALUES (%s, %s);"
        data = (super_name, sub_name)
        cursor.execute(query, data)
        return query
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route("/delete_cat")
def delete_cat():
    dbConn = None
    cursor = None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cat_name = request.args["cat_name"]
        query = """ START TRANSACTION;
                DELETE FROM evento_reposicao WHERE ean = ANY (SELECT ean FROM prod>
                DELETE FROM tem_categoria WHERE nome = %s;
                DELETE FROM planograma WHERE ean = ANY (SELECT ean FROM produto WH>
                DELETE FROM produto WHERE cat = %s;
                DELETE FROM responsavel_por WHERE nome_cat = %s;
                DELETE FROM prateleira WHERE nome = %s;
                DELETE FROM tem_outra WHERE super_categoria = %s;
                DELETE FROM tem_outra WHERE categoria = %s;
                DELETE FROM categoria_simples WHERE nome = %s;
                DELETE FROM super_categoria WHERE nome = %s;
                DELETE FROM categoria WHERE nome = %s;
                COMMIT;"""
        data = (cat_name,) * 11
        cursor.execute(query, data)
        return query
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

CGIHandler().run(app)
