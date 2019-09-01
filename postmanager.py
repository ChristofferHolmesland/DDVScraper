import requests as r
import sqlite3
import argparse
from bs4 import BeautifulSoup

URL = "https://innsyn.ddv.no/einnsyn{0}/RegistryEntry/Case?caseId={1}"
INSERT_STATEMENT = "INSERT INTO PostCase VALUES (?, ?, ?, ?, ?, ?, ?)"

parser = argparse.ArgumentParser(description="Scrape public post by any municipality using the DDV postlist system")
parser.add_argument("municipality", type=str)
parser.add_argument("--min_id", type=int)
parser.add_argument("--max_id", required=True, type=int)
parser.add_argument("--print", default="all", type=str, choices=["all", "valid", "none"])

args = parser.parse_args()
municipality = args.municipality
min_id = args.min_id or -1
max_id = args.max_id
print_option = args.print

conn = sqlite3.connect("{}.db".format(municipality))

conn.execute("CREATE TABLE IF NOT EXISTS PostCase(id INTEGER PRIMARY KEY, year INTEGER, number INTEGER, title TEXT, responsible TEXT, status TEXT, htmldocument TEXT)")
conn.commit()

if min_id == -1:
    row = conn.execute("SELECT * FROM PostCase ORDER BY id DESC LIMIT 1").fetchone()
    min_id = 0 if row is None else row[0] + 1

for i in range(min_id, max_id + 1):
    data = r.get(URL.format(municipality, i))
    valid = data.status_code == 200

    if print_option == "all" or (print_option == "valid" and valid):
        print("Case {0}, status code: {1} {2}".format(i, data.status_code, "----------" if valid else ""))
    if not valid: continue

    soup = BeautifulSoup(data.text, "html.parser")
    data_fields = soup.find("div", class_="detailsmetadatablock").find_all("div", class_="display-field")
    clean_data_fields = [x.text.strip() for x in data_fields]

    year, number = clean_data_fields[0].split("/")

    db_data = (
        i,
        int(year),
        int(number),
        clean_data_fields[1],
        clean_data_fields[2],
        clean_data_fields[3],
        data.text
    )

    conn.execute(INSERT_STATEMENT, db_data)
    conn.commit()
