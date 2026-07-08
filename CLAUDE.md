# rulespec-zm Agent Notes

This repo stores Zambia RuleSpec source registry materials, oracle references, and encoded policy rules. Zambia is a unitary state, so all encoded law lives under a single `zm/` national namespace.

## Scope

- `zm/statutes/`: Zambia Acts of Parliament — the Income Tax Act (Cap. 323) as amended, the Value Added Tax Act (Cap. 331), the Customs and Excise Act (Cap. 322), the National Pension Scheme Act (Cap. 256), the National Health Insurance Act, 2018, and other primary law needed for tax-benefit modeling.
- `zm/regulations/`: statutory instruments made under the governing Acts (Pensionable Earnings Regulations, NHI General Regulations, rate orders).
- `zm/policies/`: ZRA practice notes captured as verified reproductions of undigitized statutory instruments, and social-protection programme rules (Social Cash Transfer and the other MCDSS/MoE/MoA programmes) set administratively.
- `programs/`: declarative compose specs (one per jurisdiction/program/period).
- `data/corpus/`: source inventory, ingestion notes, provision locators, and promoted official-source extracts.
- `data/coverage/`: tax-benefit coverage backlog and source map.
- `data/oracles/`: executable or documentary comparison references. These are never legal authority.

## Do

- Treat the scope as a Zambia tax-benefit surface backed by Zambia upstream law.
- Start from the furthest upstream available source: Parliament of Zambia assented Act prints and Government Printer editions first (parliament.gov.zm serves direct PDFs; ZambiaLII AKN source PDFs are open), statutory-instrument gazette prints next, ZRA practice notes and ministry programme documentation only after the governing instrument is identified — or as verified reproductions where a primary SI print is not publicly digitized (flag this in manifest metadata).
- Add RuleSpec under `zm/statutes/`, `zm/regulations/`, or `zm/policies/` with companion `.test.yaml` files.
- Keep source law provenance in corpus artifacts and cite those corpus paths from RuleSpec modules via `module.source_verification.corpus_citation_path` (or `corpus_citation_paths` for multi-instrument modules).
- Use CY2025 as the validation year for encoded amounts (Zambia's charge year is the calendar year; the December amendment package commences 1 January). MicroZAMOD system ZM_2025 corresponds to CY2025. Indexed/annual values must be corpus-grounded, never invented.
- Keep exact oracle versions in `data/oracles/oracle-index.json`. The MicroZAMOD bundle (SOUTHMOD A4.0) is licensed and non-redistributable — never commit bundle bytes, dataset rows, or model XML; only comparison statistics and MicroZAMOD-produced values may be recorded.
- Sync `axiom-encode` and `.axiom/toolchain.toml` before substantial encoding runs.

## Do Not

- Use ZRA calculator pages, PAYE ready-reckoners, or third-party summaries as the first legal source when an Act or statutory instrument governs the rule.
- Invent, round, or interpolate any Zambian monetary amount, rate band, or threshold. Every number must come verbatim from a captured official provision.
- Migrate MicroZAMOD, EUROMOD/SOUTHMOD, or agency calculator code mechanically as RuleSpec.
- Add generated source payload dumps, formula artifacts, `parameters.yaml`, or standalone YAML fixtures outside allowed RuleSpec roots.
- Hand-copy statute text into RuleSpec without a corpus `citation_path`.
