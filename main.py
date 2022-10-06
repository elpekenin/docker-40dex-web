import config
from flask import (
    Flask,
    redirect,
    render_template,
    send_from_directory,
    url_for
)
from flask_compress import Compress
import json
import logging
from os import path
from pymongo import MongoClient
from requests import get
import subprocess

# =======
# Setup
logging.basicConfig(
    level=logging.DEBUG,
    filename="logs/log.txt",
    format="%(asctime)s -- %(levelname)s -- %(message)s",
    datefmt="%d/%b/%y %H:%M:%S",
    filemode="w"
)
logging.info("Started !!")

if config.db_uri:
    client = MongoClient(config.db_uri, serverSelectionTimeoutMS=10_000)
else:
    client = MongoClient(
        config.db_ip,
        username=config.db_user,
        password=config.db_pass,
        authSource=config.db_auth
    )

database = client["website"]

app = Flask(__name__)
Compress(app)

with open("dex-name.json", "r") as f:
    dex_cache = json.load(f)


# =======
# Funcs
def read_from_cache(query):
   return dex_cache.get(query, 0)


def get_dex(name):   
    # FIXME This will break when new pokemons get added
    return read_from_cache(name.lower())

app.jinja_env.globals["get_dex"] = get_dex


def get_name(dex):
    return read_from_cache(str(dex))

app.jinja_env.globals["get_name"] = get_name


with open("./build-timestamp", "r") as f:
    build_date = f.readline()

app.jinja_env.globals["build_date"] = build_date


try:
    commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
except:
    commit = "Couldn't find commit hash"

app.jinja_env.globals["commit"] = commit


def class_from_row(row):
    return " ".join(row.keys())

app.jinja_env.globals["class_from_row"] = class_from_row


def width_from_row(row):
    return f"min(100px, {100/(len(row)+3)}vw)"

app.jinja_env.globals["width_from_row"] = width_from_row


def parse_region(_region):
    try:
        region = int(_region) #parse to region id
        if region == 0: # default value just in case
            region = 1
    except:
        region = _region.lower()
        region = { #try parsing name to id, default to kanto
            "kanto":   1,
            "johto":   2,
            "hoenn":   3,
            "sinnoh":  4,
            "unova":   5,
            "teselia": 5,
            "kalos":   6,
            "alola":   7,
            "galar":   8
        }.get(region, 1)
    logging.debug(f"Parsed region {region} from '{_region}'")

    return region


def _get_data_from_region(region):
    # get all pokedex filtered by region
    # TODO try to make the aggregation on a single query
    _filter = {"regions": {"$all": [region]}}
    _find = lambda x: list(database[x].find(_filter, {"_id": False}))
    _data = [
        _find("40dex"),
        _find("trade-dex")
    ]

    data = []
    for i, family in enumerate(_data[0]):
        temp = {}
        for poke in family:
            if poke == "regions":
                continue

            temp[poke] = [info[i][poke] for info in _data]

        data.append(temp)

    return data


def get_40dex_page(region):
    file_path   = f"html/40dex/{region}.html"
    static_path = f"static/{file_path}"

    # Use static file if no changes were made
    if path.isfile(static_path):
        return send_from_directory("static", file_path) # return static file

    # Re-gen HTML
    data = _get_data_from_region(region)
    page = render_template(
        "40dex.html",
        data=data,
        region=region,
        max_region=8,
        path="/40dex"
    )

    # Save static file
    with open(static_path, "w") as f:
        f.write(page)

    # Return content
    return page


def _get_40dex_stats():
    dex = list(database["40dex"].find())
    total = len(dex)
    pokes = 0
    families = 0

    for row in dex:
        add = True
        for key, value in row.items():
            if key in ["_id", "regions"]:
                continue

            if value > 0:
                pokes += value
                if add:
                    families += 1
                    add = False

    return families, pokes, total


def get_40dex_stats_page():
    file_path   = "html/40dex/stats.html"
    static_path = f"static/{file_path}"

    # Use static file if no changes were made
    if path.isfile(static_path):
        return send_from_directory("static", file_path) # return static file

    # Re-gen HTML
    families, pokes, total = _get_40dex_stats()
    page = render_template(
        "40dex-stats.html",
        families=families,
        pokes=pokes,
        total=total
    )

    # Save static file
    with open(static_path, "w") as f:
        f.write(page)

    # Return content
    return page


# =======
# Routes
@app.get("/")
def hello():
    return "Hello World!"

@app.get("/40dex/stats/")
def dex_stats():
    return get_40dex_stats_page()

@app.get("/40dex/")
@app.get("/40dex/<_region>/")
def dex(_region="kanto"):
    return get_40dex_page(parse_region(_region))
