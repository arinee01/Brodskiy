from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import DC, XSD
import pandas as pd
import os

SCHEMA = Namespace("http://schema.org/")
LIDO = Namespace("http://www.lido-schema.org/")
WD = Namespace("http://www.wikidata.org/entity/")
BASE = "http://brodskiy-lod.github.io/"

g = Graph()
g.bind("dc", DC)
g.bind("xsd", XSD)
g.bind("schema", SCHEMA)
g.bind("lido", LIDO)
g.bind("wd", WD)

def add_item(subject_id, data):
    uri = URIRef(BASE + subject_id)
    
    if "title" in data:
        g.add((uri, DC.title, Literal(data["title"], datatype=XSD.string)))
    if "creator" in data:
        creator = data["creator"]
        g.add((uri, DC.creator, wd_or_literal(creator)))
    if "date" in data:
        g.add((uri, DC.date, Literal(data["date"], datatype=XSD.gYear)))
    if "description" in data:
        g.add((uri, DC.description, Literal(data["description"], datatype=XSD.string)))
    if "type" in data:
        g.add((uri, RDF.type, wd_or_literal(data["type"])))


    for field, predicate in [
        ("subject", DC.subject),
        ("language", DC.language),
        ("format", DC.format),
        ("genre", SCHEMA.genre),
        ("location", SCHEMA.location),
        ("locationCreated", SCHEMA.locationCreated),
        ("material", SCHEMA.material),
        ("function", SCHEMA.function),
        ("publisher", DC.publisher),
        ("inscription", LIDO.inscriptionTranscription),
        ("identifier", DC.identifier),
        ("dateCreated", SCHEMA.dateCreated),
        ("duration", SCHEMA.duration)
    ]:
        if field in data:
            values = ensure_list(data[field])
            for val in values:
                g.add((uri, predicate, wd_or_literal(val)))

    if "relatedTo" in data:
        for rel in data["relatedTo"]:
            g.add((uri, SCHEMA.relatedTo, URIRef(BASE + rel)))


def wd_or_literal(value):
    value = value.strip()
    if value.startswith("Q"):
        return WD[value]
    return Literal(value, datatype=XSD.string)

def ensure_list(val):
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        return [v.strip() for v in val.split(";") if v.strip()]
    return []

folder = "data/"
for file in os.listdir(folder):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(folder, file))
        for _, row in df.iterrows():
            data = row.to_dict()
            subject_id = data.pop("id", os.path.splitext(file)[0])
            add_item(subject_id, data)


g.serialize(destination="brodsky_final.ttl", format="turtle")
