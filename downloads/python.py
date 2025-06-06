
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import DC, XSD
import pandas as pd
import os

# Базовые пространства имен
SCHEMA = Namespace("http://schema.org/")
LIDO = Namespace("http://www.lido-schema.org/")
BASE = "http://brodskiy-lod.github.io/"

# Инициализация графа
g = Graph()
g.bind("dc", DC)
g.bind("xsd", XSD)
g.bind("schema", SCHEMA)
g.bind("lido", LIDO)

def add_item(subject_id, data):
    uri = URIRef(BASE + subject_id)
    g.add((uri, DC.title, Literal(data.get("title"), datatype=XSD.string)))
    g.add((uri, DC.creator, Literal(data.get("creator"), datatype=XSD.string)))
    g.add((uri, DC.date, Literal(data.get("date"), datatype=XSD.gYear)))
    g.add((uri, DC.description, Literal(data.get("description"), datatype=XSD.string)))
    g.add((uri, DC.subject, Literal(data.get("subject"), datatype=XSD.string)))
    g.add((uri, RDF.type, Literal(data.get("type"), datatype=XSD.string)))

    if "location" in data:
        g.add((uri, SCHEMA.location, Literal(data.get("location"), datatype=XSD.string)))
    if "language" in data:
        g.add((uri, DC.language, Literal(data.get("language"), datatype=XSD.string)))
    if "format" in data:
        g.add((uri, DC.format, Literal(data.get("format"), datatype=XSD.string)))
    if "genre" in data:
        g.add((uri, SCHEMA.genre, Literal(data.get("genre"), datatype=XSD.string)))
    if "locationCreated" in data:
        g.add((uri, SCHEMA.locationCreated, Literal(data.get("locationCreated"), datatype=XSD.string)))
    if "relatedTo" in data:
        for item in data["relatedTo"]:
            g.add((uri, SCHEMA.relatedTo, Literal(item, datatype=XSD.string)))
    if "inscription" in data:
        g.add((uri, LIDO.inscriptionTranscription, Literal(data.get("inscription"), datatype=XSD.string)))

# Пример структуры данных
items = [
    {
        "subject": "Brodsky_Tombstone",
        "title": "Joseph Brodsky’s tombstone",
        "creator": "Vladimir Radunsky",
        "date": "1997",
        "description": "A tombstone created by Vladimir Radunsky in memory of Joseph Brodsky.",
        "subject": "Joseph Brodsky",
        "type": "Memorial",
        "location": "Venice",
        "relatedTo": ["Memorial_plaque", "Photo_Brodsky_Venice"],
        "inscription": "Iosif Brodsky 24.V.1940–28.1.1996"
    },
    # добавьте сюда остальные элементы по аналогии
]

# Генерация графа
for item in items:
    add_item(item["subject"], item)

# Сохранение в файл
g.serialize(destination="/mnt/data/brodsky_rdf_script_output.ttl", format="turtle")
