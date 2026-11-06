# Brasil–STANAG

Mapeamento SKOS, com fontes, entre normas, sistemas, órgãos e equipamentos brasileiros e referências de padronização da OTAN (STANAGs, publicações aliadas, códigos e programas).
*SKOS mapping, with sources, between Brazilian regulations, systems, agencies and equipment and NATO standardization references.*

> [!IMPORTANT]
> **Trabalho independente, só com fontes abertas.** Não tem aval da OTAN, do Ministério da Defesa, da ABIN nem de qualquer outro órgão.
> Os STANAGs aparecem apenas pelo número, título e publicação aliada públicos (catálogo do NATO Standardization Office).
> O texto integral dos STANAGs **não** foi consultado. Os mapeamentos são **propostas de correspondência**
> (`skos:relatedMatch`, `closeMatch`, `broadMatch`), nunca equivalência oficial. O validador rejeita `skos:exactMatch` entre Brasil e OTAN.
> Os graus de sigilo brasileiros e da OTAN são modelados lado a lado, **sem** mapeamento.

## Números (v0.2.0)

| | |
|---|---|
| Mapeamentos Brasil–OTAN | 57 (46 verificados, 11 a confirmar) |
| Referências OTAN | 55, em 13 áreas |
| Conceitos brasileiros | 62 |
| Alinhamentos a ontologias externas | 56 (52 com a Common Core Ontologies, 2 com o registro EPSG, 2 com a UNSPSC) |
| Identificadores Wikidata | 58 |
| Conjuntos de dados do dados.gov.br (DCAT) | 12 |

Tabela completa: [`docs/mapeamentos.md`](docs/mapeamentos.md). Visão geral em PDF: [`docs/brasil-stanag-visao-geral.pdf`](docs/brasil-stanag-visao-geral.pdf).

## Áreas cobertas

| Área | Referências OTAN (exemplos) | Correspondentes brasileiros (exemplos) |
|---|---|---|
| Codificação | NCS, NSN, NCAGE, STANAG 3150/3151/4177 (ACodP-1), grupos FSC | SISCADE (MD), RENAVAM, NCM/SH, CTB art. 120 §2º |
| Logística | STANAG 4329 | GS1 Brasil |
| Mobilidade | MLC, STANAG 2021, 2468 (AMovP-4), 2174 (AMovP-1) | ABNT NBR 7188, malha ferroviária, SNV, SINAMOB |
| Geoespacial | STANAG 2211 (AGeoP-21), WGS 84, MGRS, STANAG 7074, 1059 | SIRGAS2000, UTM do SCN, ET-EDGV, código BRA |
| Confidencialidade | STANAG 4774, 4778, NCMS | LAI, Decreto 7.845/2012, LGPD, ICP-Brasil, e-PMG |
| Proteção | STANAG 4569, 2920 | ABNT NBR 15000, Decreto 10.030/2019 |
| Munição e armamento | STANAG 4172, 2310, 4090, 4383, 4694 | Fuzil IA2 |
| Enlaces de dados | Link 16, 11, 22 | Link-BR2 |
| Aeronaves não tripuladas | STANAG 4586, 4671 | RBAC-E nº 94 (ANAC), NCM 88.06 |
| Combustíveis | STANAG 1135, F-34, F-35 | QAV-1 (ANP) |
| Terminologia e simbologia | AAP-6, APP-6, STANAG 2116 | MD35-G-01, MD33-M-02, Estatuto dos Militares |
| Arquitetura | NAF v4, NISP (ADatP-34), MIP/MIM | e-PING, SINAMOB |

## Ontologias e vocabulários conectados

SKOS · OWL · PROV-O (autoria e data de cada mapeamento) · DCAT (dados.gov.br) · schema.org e W3C ORG (organizações) ·
[Common Core Ontologies](https://github.com/CommonCoreOntology/CommonCoreOntologies) (base BFO; classes conferidas no arquivo oficial) ·
Wikidata (IDs conferidos pela API) · registro EPSG · Sistema Harmonizado/NCM · Federal Supply Classification · UNSPSC.

## Estrutura

```
data/*.csv                     # fonte da verdade, revisável (separador "|")
  otan.csv                     # referências OTAN (metadados públicos)
  brasil.csv                   # conceitos brasileiros
  mapeamentos.csv              # correspondências Brasil–OTAN (relação, status, fonte, nota)
  alinhamentos_externos.csv    # ligações com CCO, EPSG, UNSPSC
  conjuntos_dados.csv          # conjuntos do dados.gov.br
ontology/core.ttl              # vocabulário, graus de sigilo (sem mapeamento)
ontology/generated/*.ttl       # gerado por scripts/build.py — não editar
shapes/brasil-stanag.shacl.ttl # regras de qualidade
lean/Invariantes.lean          # gerado: invariantes dos dados provados em Lean 4
scripts/build.py               # CSV → Turtle, docs e Lean
scripts/validate.py            # SHACL + checagem de IRIs órfãos
```

## Usar

```bash
python3 scripts/build.py              # gera ontology/generated, docs e lean
uv run python scripts/validate.py     # valida (SHACL + IRIs órfãos)
cd lean && lean Invariantes.lean      # opcional: Lean 4 v4.35.0
```

## Verificações

- **SHACL**: fonte obrigatória, autoria PROV-O, status válido, proibição de `exactMatch` Brasil–OTAN, sem IRIs locais órfãos.
- **Lean 4**: `lean/Invariantes.lean` prova por `decide` que não há `exactMatch`, que todo mapeamento tem fonte e que os IDs são únicos.
  Isso confere a consistência dos **dados**, não se cada correspondência está semanticamente correta.
- **Testes negativos**: um mapeamento `exactMatch` inserido de propósito é rejeitado pelo SHACL e pelo Lean.
- **Dois parsers independentes** (rdflib e um leitor Turtle em Rust) leem o mesmo número de triplas.

## Status dos mapeamentos

- `verificado`: os elementos foram conferidos em fonte pública (catálogo NSO, legislação no Planalto, Wikidata, registros oficiais).
- `a-confirmar`: correspondência temática ou hipótese de trabalho, ou algum título/número ainda não confirmado.

## Contexto

Este mapeamento nasceu de contribuições a consultas públicas no Brasil Participativo (2026), incluindo
erratas publicadas quando a conferência das fontes encontrou erros. Correções são bem-vindas por issue ou pull request,
sempre com fonte pública.

## Licença

Dados e documentação: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Código (`scripts/`): MIT.

Autor: Dionisio Chiuratto Agourakis
