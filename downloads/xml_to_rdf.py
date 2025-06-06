from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import DCTERMS, RDF, XSD
from lxml import etree

file_path = "watermark.xml"

tree = etree.parse(file_path)
root = tree.getroot()
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

g = Graph()

EX = Namespace("http://brodskiy-lod.github.io/")
g.bind("ex", EX)
g.bind("dcterms", DCTERMS)

doc_uri = EX['Watermark']

title_el = root.find('.//tei:titleStmt/tei:title', namespaces=ns)
if title_el is not None and title_el.text:
    g.add((doc_uri, DCTERMS.title, Literal(title_el.text)))

author_el = root.find('.//tei:titleStmt/tei:author', namespaces=ns)
if author_el is not None and author_el.text:
    g.add((doc_uri, DCTERMS.creator, Literal(author_el.text)))

date_el = root.find('.//tei:editionStmt/tei:edition/tei:date', namespaces=ns)
if date_el is not None and date_el.text:
    try:
        g.add((doc_uri, DCTERMS.date, Literal(date_el.text, datatype=XSD.date)))
    except:
        g.add((doc_uri, DCTERMS.date, Literal(date_el.text)))

source_el = root.find('.//tei:sourceDesc/tei:p', namespaces=ns)
if source_el is not None and source_el.text:
    g.add((doc_uri, DCTERMS.source, Literal(source_el.text)))

for div in root.findall('.//tei:div[@type="chapter"]', namespaces=ns):
    chap_n = div.get('n')
    if not chap_n:
        continue
    chapter_uri = EX[f'watermark_chapter_{chap_n}']
    g.add((chapter_uri, RDF.type, EX.Chapter))
    g.add((chapter_uri, DCTERMS.isPartOf, doc_uri))
    
    head_el = div.find('tei:head', namespaces=ns)
    if head_el is not None and head_el.text:
        g.add((chapter_uri, DCTERMS.title, Literal(head_el.text)))
    
    for i, p_el in enumerate(div.findall('tei:p', namespaces=ns), start=1):
        paragraph_uri = EX[f'watermark_chapter_{chap_n}_para_{i}']
        g.add((paragraph_uri, RDF.type, EX.Paragraph))
        g.add((paragraph_uri, DCTERMS.isPartOf, chapter_uri))
        if p_el.text:
            g.add((paragraph_uri, RDF.value, Literal(p_el.text)))

g.serialize("watermark_1.rdf", format='turtle')