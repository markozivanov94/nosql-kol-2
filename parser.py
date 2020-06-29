import pymongo
import xml.etree.ElementTree as ET
import json

# Ucitavanje xml/osm fajla
context = ET.iterparse("macedonia-latest.osm", events=("start", "end"))

nodes = []
node = None

# Parsiranje xml u json
for event, elem in context:
    if event == "start":
        # Zanimaju nas samo node ili tag elementi
        if elem.tag in ["node", "tag"]:
            if elem.tag == "tag":
                # Setujemo tag u datom nodu
                nodes[node]["tags"][elem.attrib["k"]] = elem.attrib["v"]
            else:
                # Kreiramo novi node
                attrs = elem.attrib
                node = len(nodes)
                nodes.append({
                    "id": attrs["id"],
                    "location": {
                        "type": "Point",
                        "coordinates":{
                            "lat": float(attrs["lat"]),
                            "lon": float(attrs["lon"])  
                        }
                    },
                    "tags": {}
                })
    # Cistimo memoriju
    if event == "end":
        elem.clear()
    # Ako je stigao do way/relation zavrsio je sve nodove
    if elem.tag in ["way", "relation"]:
        break

# Cuvamo u json
with open("nodes.json", "w") as file:
    json.dump(nodes, file, indent=4, ensure_ascii=False)

# Otvaramo konekciju sa bazom
client = pymongo.MongoClient(port=27017)
# Selektujemo document (Ako ne postoji, napravi ga)
db = client.osm

# Cuvamo u bazu
db.nodes.insert_many(nodes)

# Setujemo index lokacije da je GEOSPHERE
db.nodes.create_index([("location", pymongo.GEOSPHERE)])
