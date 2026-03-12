import sqlite3

facts = [
"Свет от Солнца до Земли идет около 8 минут.",
"Число π имеет бесконечное количество цифр.",
"Человеческий мозг содержит около 86 миллиардов нейронов.",
"Самый древний университет — Болонский, основан в 1088 году.",
"ДНК человека совпадает с бананом примерно на 60%."
]

conn = sqlite3.connect("database.db")
cur = conn.cursor()

for fact in facts:
    cur.execute("INSERT INTO facts(text, shown) VALUES(?,0)", (fact,))

conn.commit()
conn.close()