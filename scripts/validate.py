"""Valida todos os arquivos de ontology/**/*.ttl contra as shapes SHACL e checa que todo IRI
local usado está declarado (sem conceitos órfãos)."""
from pathlib import Path
import sys

from pyshacl import validate
from rdflib import Graph, URIRef
from rdflib.namespace import RDF

ROOT = Path(__file__).resolve().parent.parent
LOCAL = "https://github.com/josaum/brasil-stanag-ontology/"


def load() -> Graph:
    g = Graph()
    for f in sorted((ROOT / "ontology").rglob("*.ttl")):
        g.parse(f)
    return g


def main() -> int:
    data = load()
    shapes = Graph().parse(ROOT / "shapes" / "brasil-stanag.shacl.ttl")
    conforms, _, report = validate(data, shacl_graph=shapes, inference="none")
    print(report if not conforms else "SHACL: conforme")

    declared = set(data.subjects(RDF.type, None))
    used = {o for o in data.objects() if isinstance(o, URIRef) and str(o).startswith(LOCAL)}
    orphans = sorted(str(u) for u in used - declared)
    if orphans:
        print("IRIs locais usados sem declaração:", *orphans, sep="\n  ")
    print(f"triplas: {len(data)}")
    return 0 if conforms and not orphans else 1


if __name__ == "__main__":
    sys.exit(main())
