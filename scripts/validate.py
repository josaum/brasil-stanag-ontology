"""Valida a ontologia contra as shapes SHACL e gera a tabela de mapeamentos (docs/mapeamentos.md)."""
from pathlib import Path
import sys

from pyshacl import validate
from rdflib import Graph, Namespace
from rdflib.namespace import RDFS, SKOS

ROOT = Path(__file__).resolve().parent.parent
BST = Namespace("https://github.com/josaum/brasil-stanag-ontology/ns#")


def label(g: Graph, node) -> str:
    for lbl in g.objects(node, SKOS.prefLabel):
        return str(lbl)
    return str(node)


def main() -> int:
    data = Graph().parse(ROOT / "ontology" / "brasil-stanag.ttl")
    shapes = Graph().parse(ROOT / "shapes" / "brasil-stanag.shacl.ttl")
    conforms, _, report = validate(data, shacl_graph=shapes, inference="none")
    print(report if not conforms else "SHACL: conforme")

    rows = []
    for m in sorted(data.subjects(predicate=BST.conceitoSTANAG)):
        br = data.value(m, BST.conceitoBrasileiro)
        st = data.value(m, BST.conceitoSTANAG)
        rel = str(data.value(m, BST.relacao)).split("#")[-1]
        num = data.value(st, BST.numero)
        pub = data.value(st, BST.publicacaoAliada)
        stname = (f"STANAG {num} — " if num else "") + label(data, st) + (f" ({pub})" if pub else "")
        note = data.value(m, RDFS.comment) or ""
        rows.append(f"| {m.split('#')[-1]} | {label(data, br)} | {rel} | {stname} | {data.value(m, BST.status)} | {note} |")

    out = ROOT / "docs" / "mapeamentos.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(
        "# Mapeamentos (gerado por `scripts/validate.py`)\n\n"
        "| ID | Conceito brasileiro | Relação SKOS | STANAG / referência | Status | Nota |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )
    print(f"{len(rows)} mapeamentos -> {out.relative_to(ROOT)}")
    return 0 if conforms else 1


if __name__ == "__main__":
    sys.exit(main())
