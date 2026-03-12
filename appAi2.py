from flask import Flask, render_template, jsonify
import random
import sqlite3
import requests
import json
from openai import OpenAI

app = Flask(__name__)

client = OpenAI()

GENERAL_PROMPT = """
You are an expert in science facts and quizzes.
Return answer ONLY in JSON format with fields:
category, question, answer1, answer2, answer3, answer4, correct_answer
"""


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



def get_wikipedia_fact():

    url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    response = requests.get(url)

    data = response.json()

    return data["extract"]



def ai_prompt(current_prompt):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":GENERAL_PROMPT},
            {"role":"user","content":current_prompt}
        ]
    )

    text = response.choices[0].message.content

    return json.loads(text)



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/fact")
def fact():

    fact = get_wikipedia_fact()

    return jsonify({"fact": fact})


@app.route("/ai_fact")
def ai_fact():

    question = ai_prompt("Give next question in category FACTS")

    return jsonify(question)



if __name__ == "__main__":
    init_db()
    app.run(debug=True)

