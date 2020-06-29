from pymongo import MongoClient
import json

def find_streets(collection, coords, radius):
    # Pronadji sve u datom radijusu
    streets = collection.find(
        {
            "location":
                {"$near":
                    {
                        "$geometry": {"coordinates": coords},
                        "$maxDistance": radius
                    }
                 }
        },
        {
            # Isvlacimo samo tagove
            "tags": 1
        }
    )

    new_streets = set()
    for s in streets:
        # Ako postoji addr:street
        if "addr:street" in s["tags"]:
            new_streets.add(s["tags"]["addr:street"])

    return new_streets

coords = [42.008325, 21.367214]
radius = 3000

# Otvaramo konekciju sa bazom
client = MongoClient(port=27017)
# Biramo dokument
db = client.osm

print(find_streets(db.nodes, coords, radius))
