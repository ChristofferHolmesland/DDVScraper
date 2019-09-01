import os
import sqlite3
from flask import Flask, request, redirect

app = Flask(__name__)

script_folder = os.path.dirname(os.path.realpath(__file__))
dbs = [f.replace(".db", "") for f in os.listdir(script_folder) if f.endswith(".db")]

@app.route("/")
def home():
    municipality = request.args.get("m")
    case_id = request.args.get("id")

    if case_id is None or municipality is None:
        return "Use endpoint /?m=MUNICIPALITY&?id=CASE_ID to view a case"

    if not municipality in dbs:
        return "Invalid municipality, try: " + ", ".join(dbs)

    result = "Invalid case id"
    conn = sqlite3.connect("{}.db".format(municipality))

    row = conn.execute("SELECT htmldocument FROM PostCase WHERE id={}".format(case_id)).fetchone()
    if row is not None:
        result = row[0]

    conn.close()

    return result

@app.route("/<path:path>")
def external_redirect(path):
    return redirect("https://innsyn.ddv.no/{}".format(path))