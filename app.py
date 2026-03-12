

from flask import Flask, render_template, jsonify
import random
import sqlite3
import requests

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS facts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        shown INTEGER
    )
    """)

    conn.commit()
    conn.close()

def get_random_fact():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM facts WHERE shown = 0")
    facts = cur.fetchall()

    if not facts:
        cur.execute("UPDATE facts SET shown = 0")
        conn.commit()
        cur.execute("SELECT * FROM facts")

        facts = cur.fetchall()

    fact = random.choice(facts)

    cur.execute("UPDATE facts SET shown = 1 WHERE id=?", (fact[0],))
    conn.commit()

    conn.close()

    return fact[1]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fact")
def fact():

    try:
        fact = get_random_fact()
    except:
        fact = "no facts yet"

    return jsonify({"fact": fact})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)