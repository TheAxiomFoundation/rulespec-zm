# rulespec-zm

Zambia RuleSpec source registry.

This repository targets the Zambia tax-benefit surface: national income tax (PAYE) under the Income Tax Act (Cap. 323), the turnover tax, National Pension Scheme Authority (NAPSA) contributions under the National Pension Scheme Act (Cap. 256), National Health Insurance (NHIMA) contributions under the National Health Insurance Act, 2018 and its Regulations, value added tax (Cap. 331), excise duties (Cap. 322), and the cash and in-kind transfer programmes needed for household-level calculations (Social Cash Transfer, Supporting Women's Livelihood, Keeping Girls in School, Home Grown School Meal, Farmer Input Support Programme, Food Security Pack). Zambia is a unitary state, so all encoded law lives under a single `zm/` national namespace.

Zambia's charge year is the calendar year (1 January to 31 December). The validation year for encoded amounts is **CY2025**; effective dates follow the amending Act's commencement (typically 1 January per the December amendment package).

## Source priority

Policy must come from the furthest upstream available source.

1. Acts of Parliament assented prints (Parliament of Zambia; Government Printer; Zambia Gazette Acts supplements) and Government-Printer revised editions — the authentic text of the Income Tax Act (Cap. 323), the Value Added Tax Act (Cap. 331), the Customs and Excise Act (Cap. 322), the National Pension Scheme Act (Cap. 256), the National Health Insurance Act, 2018, and their amending Acts; statutory instruments (Gazette supplements) for rates and ceilings prescribed by regulation.
2. Zambia Revenue Authority (ZRA) rate tables, PAYE guides, and practice notes only after the governing Act is identified.
3. Ministry of Community Development and Social Services, Ministry of Education, and Ministry of Agriculture official programme documentation for the transfer programmes, whose rules are set administratively rather than by Act.
4. Oracles only for household-level parity tests against an external source that can calculate the same household case, never as law.

## Oracle scope

An oracle is an executable, pinned external calculator that accepts household-level inputs and returns household-level tax-benefit outputs comparable to Axiom outputs. Aggregate simulators, distributional reports, parameter documentation, and public model summaries are not oracles for RuleSpec parity, even when they are useful as background references.

The Zambia household oracle is **MicroZAMOD**, the SOUTHMOD tax-benefit microsimulation model for Zambia (UNU-WIDER). UNU-WIDER approved access on 2026-07-07, and MicroZAMOD is wired by eight per-case comparison suites in [axiom-oracles](https://github.com/TheAxiomFoundation/axiom-oracles) (`comparisons/zm-*.yaml`), run on system ZM_2025; zm-napsa-contributions and zm-sct run ZM_2024. The SOUTHMOD_A4.0 Adhesion Agreement bars giving the bundle to third parties, so those suites run only on the machine that holds it, never on shared CI; the committed reports are the record. `data/oracles/oracle-index.json` pins the bundle hash and lists each suite with the outputs it compares.

## Listing gates

This repo carries `app_visibility = "experimental"` in `.axiom/registry.toml` and stays out of app surfaces until:

1. The encoded surface covers the flagship calculation (PAYE gross-to-net for a formal employee) end to end with companion tests.
2. Oracle parity suites exist and pass against MicroZAMOD for the encoded surface. Status: **partially met**. Eight MicroZAMOD suites compare eight of the 18 encoded modules, and all 36 comparisons on 30 synthetic cases match, with none dispositioned (see `data/oracles/oracle-index.json`). Not all of that is independent validation: zm-paye-rate-schedule, zm-vat and zm-excise-ad-valorem feed the model's own base to the module, so they test rates and schedule arithmetic rather than the base, and zm-dispy and zm-turnover keep their cases in zones where both sides agree; the known differences outside those zones are oracle-side findings in axiom-oracles. The compared modules carry manual-attestation manifests and are not supervised-encoder output ([rulespec-zm#24](https://github.com/TheAxiomFoundation/rulespec-zm/issues/24)), so the suites must be re-run after the encoder backfill.
3. Citation paths are stable (chapter-number vs act-number form resolved against the current Government-Printer edition).
