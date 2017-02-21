import sqlite3
import csv
from pprint import pprint

sqlite_file = 'osm_hamburg.db'

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

# Create table fom nodes
cur.execute('DROP TABLE IF EXISTS nodes')
conn.commit()

cur.execute('''
    CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT)
    ''')
conn.commit()

nodes = '/Users/lt/Git/portfolio-projects/open_streetmap_data_wrangling/data/nodes.csv'
with open(nodes,'rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['lat'], i['lon'], i['user'].decode("utf-8"), i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()

# Create table fom nodes_tags
cur.execute('DROP TABLE IF EXISTS nodes_tags')
conn.commit()

cur.execute('''
    CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id))
    ''')
conn.commit()

nodes_tags = '/Users/lt/Git/portfolio-projects/open_streetmap_data_wrangling/data/nodes_tags.csv'
with open(nodes_tags,'rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'],i['value'].decode("utf-8"), i['type']) for i in dr]

cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
conn.commit()

# Create table fom ways
cur.execute('DROP TABLE IF EXISTS ways')
conn.commit()

cur.execute('''
    CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT)
    ''')
conn.commit()

ways = '/Users/lt/Git/portfolio-projects/open_streetmap_data_wrangling/data/ways.csv'
with open(ways,'rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['user'].decode("utf-8"), i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
conn.commit()

# Create table fom ways_tags
cur.execute('DROP TABLE IF EXISTS ways_tags')
conn.commit()

cur.execute('''
    CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id))
    ''')
conn.commit()

ways_tags = '/Users/lt/Git/portfolio-projects/open_streetmap_data_wrangling/data/ways_tags.csv'
with open(ways_tags,'rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'],i['value'].decode("utf-8"), i['type']) for i in dr]

cur.executemany("INSERT INTO ways_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
conn.commit()

# Create table fom ways_nodes
cur.execute('DROP TABLE IF EXISTS ways_nodes')
conn.commit()

cur.execute('''
    CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
    )
    ''')
conn.commit()

ways_nodes = '/Users/lt/Git/portfolio-projects/open_streetmap_data_wrangling/data/ways_nodes.csv'
with open(ways_nodes,'rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db)
conn.commit()


conn.close()