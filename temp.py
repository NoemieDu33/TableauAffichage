import mysql.connector
import sys

conn = ""
def connect_db():
    try:
        global conn
        conn = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="profs"
        )
    except mysql.connector.Error as e:
        print("--------------------")
        print(f"Error connecting to MySQL Platform: {e}")
        print(f"Tentative de connexion à la Database: ratée!")
        print("--------------------")
        sys.exit(1)
    cur = conn.cursor(buffered=True)
    return cur

cur = connect_db()
cur.execute(f"SELECT `nom_prof` FROM `liste_profs`;")
listedata=[e for e in cur]
for e in listedata:
    print(e[0])
conn.close()

input()
