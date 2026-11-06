"""Gera a ontologia (ontology/generated/*.ttl), a documentação (docs/) e o arquivo Lean de
invariantes (lean/Invariantes.lean) a partir de data/*.csv. Somente biblioteca padrão."""
from __future__ import annotations

import csv
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GEN = ROOT / "ontology" / "generated"

PREFIXES = """@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix dct:    <http://purl.org/dc/terms/> .
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix org:    <http://www.w3.org/ns/org#> .
@prefix schema: <https://schema.org/> .
@prefix bst:    <https://github.com/josaum/brasil-stanag-ontology/ns#> .
@prefix br:     <https://github.com/josaum/brasil-stanag-ontology/br#> .
@prefix st:     <https://github.com/josaum/brasil-stanag-ontology/stanag#> .
@prefix ext:    <https://github.com/josaum/brasil-stanag-ontology/ext#> .
@prefix ds:     <https://github.com/josaum/brasil-stanag-ontology/dataset#> .
@prefix wd:     <http://www.wikidata.org/entity/> .
@prefix cco:    <https://www.commoncoreontologies.org/> .
@prefix epsg:   <http://www.opengis.net/def/crs/EPSG/0/> .

"""

SCHEMA_TYPES = {
    "orgao-publico": "schema:GovernmentOrganization , org:Organization",
    "forca-armada": "schema:GovernmentOrganization , org:Organization",
    "empresa-publica": "schema:Corporation , org:Organization",
    "empresa": "schema:Corporation , org:Organization",
    "organizacao": "org:Organization",
    "pais": "schema:Country",
}


def rows(name: str) -> list[dict]:
    with open(DATA / name, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="|"))


def lit(s: str, lang: str | None = None) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"@{lang}' if lang else f'"{s}"'


def source(s: str) -> str:
    return f"<{s}>" if s.startswith("http") else lit(s)


def build() -> dict:
    GEN.mkdir(parents=True, exist_ok=True)
    otan, brasil, maps = rows("otan.csv"), rows("brasil.csv"), rows("mapeamentos.csv")
    ext_rows, datasets = rows("alinhamentos_externos.csv"), rows("conjuntos_dados.csv")
    known = {r["curie"] for r in otan} | {r["curie"] for r in brasil}

    out = [PREFIXES]
    for r in otan:
        t = [f'{r["curie"]} a bst:ReferenciaOTAN , skos:Concept', f'skos:prefLabel {lit(r["titulo"], "en" if not r["titulo"].startswith(("Munição", "Enlace", "Código")) else "pt-BR")}',
             f'bst:area {lit(r["area"])}']
        if r["numero"]:
            t.append(f'bst:numero {lit(r["numero"])}')
        if r["publicacao"]:
            t.append(f'bst:publicacaoAliada {lit(r["publicacao"])}')
        if r["wikidata"]:
            t.append(f'skos:{"exactMatch" if r["wd_rel"] == "exact" else "relatedMatch"} wd:{r["wikidata"]}')
        if r["nota"]:
            t.append(f'skos:note {lit(r["nota"], "pt-BR")}')
        out.append(" ;\n    ".join(t) + " .\n")
    (GEN / "otan.ttl").write_text("\n".join(out), encoding="utf-8")

    out = [PREFIXES]
    for r in brasil:
        types = "bst:ConceitoBrasileiro , skos:Concept" + (f' , {SCHEMA_TYPES[r["tipo"]]}' if r["tipo"] in SCHEMA_TYPES else "")
        t = [f'{r["curie"]} a {types}', f'skos:prefLabel {lit(r["rotulo"], "pt-BR")}', f'bst:tipo {lit(r["tipo"])}']
        if r["wikidata"]:
            t.append(f'skos:exactMatch wd:{r["wikidata"]}')
        if r["fonte"]:
            t.append(f'dct:source {source(r["fonte"])}')
        if r["nota"]:
            t.append(f'skos:note {lit(r["nota"], "pt-BR")}')
        out.append(" ;\n    ".join(t) + " .\n")
    (GEN / "brasil.ttl").write_text("\n".join(out), encoding="utf-8")

    out = [PREFIXES]
    for m in maps:
        assert m["brasil"] in known and m["otan"] in known, m["id"]
        t = [f'bst:{m["id"]} a bst:Mapeamento', f'bst:conceitoBrasileiro {m["brasil"]}', f'bst:conceitoOTAN {m["otan"]}',
             f'bst:relacao skos:{m["relacao"]}', f'bst:status {lit(m["status"])}',
             "prov:wasAttributedTo bst:autor", f'prov:generatedAtTime "{date(2026, 11, 6).isoformat()}"^^xsd:date']
        t += [f"dct:source {source(s.strip())}" for s in m["fonte"].split(";") if s.strip()]
        if m["nota"]:
            t.append(f'rdfs:comment {lit(m["nota"], "pt-BR")}')
        out.append(" ;\n    ".join(t) + " .\n")
        out.append(f'{m["brasil"]} skos:{m["relacao"]} {m["otan"]} .\n')  # projeção SKOS direta
    (GEN / "mapeamentos.ttl").write_text("\n".join(out), encoding="utf-8")

    out = [PREFIXES]
    for r in ext_rows:
        assert r["local"] in known, r["local"]
        out.append(f'{r["local"]} skos:{r["relacao"]} {r["externo"]} .  # {r["nota"]}\n')
    (GEN / "externos.ttl").write_text("\n".join(out), encoding="utf-8")

    out = [PREFIXES]
    for d in datasets:
        t = [f'ds:{d["id"]} a dcat:Dataset', f'dct:identifier {lit(d["id"])}', f'dct:title {lit(d["titulo"], "pt-BR")}',
             f'dct:publisher {lit(d["organizacao"])}']
        if d["slug"]:
            t.append(f'dcat:landingPage <https://dados.gov.br/dados/conjuntos-dados/{d["slug"]}>')
        t += [f"dct:subject {c.strip()}" for c in d["conceitos"].split(",")]
        out.append(" ;\n    ".join(t) + " .\n")
    (GEN / "conjuntos_dados.ttl").write_text("\n".join(out), encoding="utf-8")

    stats = {
        "referencias_otan": len(otan),
        "conceitos_brasileiros": len(brasil),
        "mapeamentos": len(maps),
        "verificados": sum(m["status"] == "verificado" for m in maps),
        "a_confirmar": sum(m["status"] == "a-confirmar" for m in maps),
        "alinhamentos_externos": len(ext_rows),
        "cco": sum(r["externo"].startswith("cco:") for r in ext_rows),
        "wikidata": sum(bool(r["wikidata"]) for r in otan + brasil),
        "conjuntos_dados": len(datasets),
        "areas": Counter(r["area"] for r in otan),
    }
    write_lean(maps)
    return stats


def write_lean(maps: list[dict]) -> None:
    """Gera um arquivo Lean que verifica (por decide) invariantes estruturais dos mapeamentos.
    Escopo: confere a consistência dos DADOS, não a correção semântica das correspondências."""
    rel = {"relatedMatch": ".related", "closeMatch": ".close", "broadMatch": ".broad", "narrowMatch": ".narrow", "exactMatch": ".exact"}
    st = {"verificado": ".verificado", "a-confirmar": ".aConfirmar"}
    entries = ",\n  ".join(
        f'⟨"{m["id"]}", {rel[m["relacao"]]}, {st[m["status"]]}, {len([s for s in m["fonte"].split(";") if s.strip()])}⟩' for m in maps
    )
    (ROOT / "lean").mkdir(exist_ok=True)
    (ROOT / "lean" / "Invariantes.lean").write_text(f"""/-
  Gerado por scripts/build.py — NÃO editar à mão.
  Verifica, por `decide`, invariantes estruturais dos {len(maps)} mapeamentos de data/mapeamentos.csv.
  Escopo: consistência dos dados (sem exactMatch, ao menos uma fonte, IDs únicos).
  NÃO verifica se cada correspondência está semanticamente correta.
-/
inductive Relacao | related | close | broad | narrow | exact
  deriving DecidableEq, Repr
inductive Status | verificado | aConfirmar
  deriving DecidableEq, Repr

structure Mapeamento where
  id : String
  relacao : Relacao
  status : Status
  nFontes : Nat
  deriving Repr

def mapeamentos : List Mapeamento := [
  {entries}
]

theorem sem_exactMatch : mapeamentos.all (fun m => m.relacao != .exact) = true := by decide
theorem toda_correspondencia_tem_fonte : mapeamentos.all (fun m => m.nFontes ≥ 1) = true := by decide
theorem ids_unicos : (mapeamentos.map (·.id)).eraseDups.length = mapeamentos.length := by decide
theorem total : mapeamentos.length = {len(maps)} := by decide
""", encoding="utf-8")


def write_docs(stats: dict) -> None:
    import re
    maps, otan, brasil = rows("mapeamentos.csv"), {r["curie"]: r for r in rows("otan.csv")}, {r["curie"]: r for r in rows("brasil.csv")}
    def otan_label(c):
        r = otan[c]
        return (f'STANAG {r["numero"]} — ' if r["numero"] else "") + r["titulo"] + (f' ({r["publicacao"]})' if r["publicacao"] else "")
    lines = ["# Mapeamentos (gerado por `scripts/build.py`)", "",
             f'{stats["mapeamentos"]} mapeamentos ({stats["verificados"]} verificados, {stats["a_confirmar"]} a confirmar).', "",
             "| ID | Conceito brasileiro | Relação | Referência OTAN | Área | Status | Nota |", "|---|---|---|---|---|---|---|"]
    for m in maps:
        lines.append(f'| {m["id"]} | {brasil[m["brasil"]]["rotulo"]} | {m["relacao"]} | {otan_label(m["otan"])} | {otan[m["otan"]]["area"]} | {m["status"]} | {m["nota"]} |')
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "mapeamentos.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    s = build()
    write_docs(s)
    for k, v in s.items():
        print(f"{k}: {dict(v) if isinstance(v, Counter) else v}")
