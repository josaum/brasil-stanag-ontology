# Brasil–STANAG

Mapeamento SKOS, com fontes, entre normas e sistemas brasileiros e acordos de padronização da OTAN (STANAGs).
*SKOS mapping, with sources, between Brazilian regulations/systems and NATO standardization agreements (STANAGs).*

> [!IMPORTANT]
> **Trabalho independente, só com fontes abertas.** Não tem aval da OTAN, do Ministério da Defesa, da ABIN nem de qualquer outro órgão.
> Os STANAGs aparecem apenas pelo número, título e publicação aliada públicos (catálogo do NATO Standardization Office).
> O texto integral dos STANAGs **não** foi consultado. Os mapeamentos são **propostas de correspondência**
> (`skos:relatedMatch` / `skos:closeMatch`), nunca equivalência oficial. O validador rejeita `skos:exactMatch`.

## Áreas cobertas

| Área | STANAG / referência | Correspondentes brasileiros |
|---|---|---|
| Codificação | STANAG 3150, 3151, 4177 (ACodP-1) | SISCADE (MD), RENAVAM, CTB art. 120 §2º |
| Mobilidade | STANAG 2021 (MLC), 2468 (AMovP-4), 2174 (AMovP-1) | ABNT NBR 7188, malha ferroviária, SNV, SINAMOB (Lei 11.631/2007) |
| Geoespacial | STANAG 2211 (AGeoP-21) | SIRGAS2000 (IBGE) |
| Confidencialidade | STANAG 4774 (ADatP-4774), 4778 (ADatP-4778) | LAI + Decreto 7.845/2012, ICP-Brasil |
| Proteção de blindados | STANAG 4569 (AEP-55) | ABNT NBR 15000, Decreto 10.030/2019 |
| Arquitetura | NAF v4, NISP (ADatP-34), MIM (MIP) | e-PING, SINAMOB |

A tabela completa, gerada a partir da ontologia, está em [`docs/mapeamentos.md`](docs/mapeamentos.md).

## Estrutura

```
ontology/brasil-stanag.ttl        # conceitos e mapeamentos (Turtle, SKOS + OWL)
shapes/brasil-stanag.shacl.ttl    # regras de qualidade (fonte obrigatória, sem exactMatch, status)
scripts/validate.py               # valida com SHACL e gera docs/mapeamentos.md
```

## Validar

```bash
uv run python scripts/validate.py
```

## Status dos mapeamentos

- `verificado`: o número e o título do STANAG e a norma brasileira foram conferidos em fonte pública.
- `a-confirmar`: correspondência temática ou hipótese de trabalho. Precisa de revisão.

## Contexto

Este mapeamento nasceu de contribuições a consultas públicas no Brasil Participativo (2026), incluindo
erratas publicadas quando a conferência das fontes encontrou erros. Correções são bem-vindas por issue ou pull request,
sempre com fonte pública.

## Licença

Dados e documentação: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Código (`scripts/`): MIT.

Autor: Dionisio Chiuratto Agourakis
