# DDVScraper
Scrape post from any Norwegian municipality using the DDV post list system

Update: After the merging of some municipalities the script no longer works as they have moved to a different system.

## Info
Every Norwegian municipality has a public list of sent and recieved post, like [Mandal Kommune](https://innsyn.ddv.no/einnsynMAN).
Several of the municipalities in the county Vest Agder uses a system by [DDV](https://ddv.no) to publish the post. Post is generally
added to the list 2-4 days after it is sent or recieved. If you visit their website to view the list, there is a limit to how far back
in time you can go (typically a couple of months). Every post entry in the list is associated with a case. While experimenting with
their website, I discovered that it is possible to view casesseveral years back. The earliest case I found is from 2007 in Kvinesdal.
[postmanager.py](postmanager.py) scrapes their website to find every public case that can still be viewed.

A simple Flask application, [postserver.py](postserver.py), is included to make the process of viewing and navigating between the
different municipalities easier.

## Requirements
- [Python](https://www.python.org)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://2.python-requests.org/en/master/)
- Optional: [Flask](https://palletsprojects.com/p/flask/), if you want a simple interface to view cases.

## Running
#### postmanager.py
```
python postmanager.py municipality --n=1000
```
- municipality, the prefix used by the website, e.g. MAN for Mandal, LIN for Lindesnes and KVI for Kvinesdal. If you want to search multiple municipalities you can seperate them by a comma, e.g. "MAN,LIN,KVI".
- Optional: min_id, the first id to check. If not supplied, it will start from the previously checked id of that municipality,
or 0 if this is the first search. Many of them start at 15000+, except Kvinesdal which should be searched from 0.
- Optional: max_id, the last id to check. You should check the website for your municipality to get an idea of what the max should be.
As of now this should not be greater than 45000 for most of them.
- Optional: n, how many new cases to check.
- Optional: print, decides what kind of information is printed while searching. Options: "all", "valid", "none". If "valid" is
used then only valid cases are printed. If every case is printed, then "--------" is printed next to valid cases to differentiate
them.

Note: One of the optional arguments max_id and n needs to be supplied.

#### postserver.py
```
# set enviroment variable FLASK_APP to "postserver.py"
flask run
```
