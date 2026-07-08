# rulespec-zm

Zambia RuleSpec source registry.

This repository targets the Zambia tax-benefit surface: national income tax (PAYE) under the Income Tax Act (Cap. 323), the turnover tax, National Pension Scheme Authority (NAPSA) contributions under the National Pension Scheme Act (Cap. 256), National Health Insurance (NHIMA) contributions under the National Health Insurance Act, 2018 and its Regulations, value added tax (Cap. 331), excise duties (Cap. 322), and the cash and in-kind transfer programmes needed for household-level calculations (Social Cash Transfer, Supporting Women's Livelihood, Keeping Girls in School, Home Grown School Meal, Farmer Input Support Programme, Food Security Pack). Zambia is a unitary state, so all encoded law lives under a single `zm/` national namespace.

Zambia's charge year is the calendar year (1 January to 31 December). The validation year for encoded amounts is **CY2025**; effective dates follow the amending Act's commencement (typically 1 January per the December amendment package).

## Source Priority

Policy must come from the furthest upstream available source.

1. Acts of Parliament assented prints (Parliament of Zambia; Government Printer; Zambia Gazette Acts supplements) and Government-Printer revised editions — the authentic text of the Income Tax Act (Cap. 323), the Value Added Tax Act (Cap. 331), the Customs and Excise Act (Cap. 322), the National Pension Scheme Act (Cap. 256), the National Health Insurance Act, 2018, and their amending Acts; statutory instruments (Gazette supplements) for rates and ceilings prescribed by regulation.
2. Zambia Revenue Authority (ZRA) rate tables, PAYE guides, and practice notes only after the governing Act is identified.
3. Ministry of Community Development and Social Services, Ministry of Education, and Ministry of Agriculture official programme documentation for the transfer programmes, whose rules are set administratively rather than by Act.
4. Oracles only for household-level parity tests against an external source that can calculate the same household case, never as law.

## Oracle Scope

An oracle is an executable, pinned external calculator that accepts household-level inputs and returns household-level tax-benefit outputs comparable to Axiom outputs. Aggregate simulators, distributional reports, parameter documentation, and public model summaries are not oracles for RuleSpec parity, even when they are useful as background references.

MicroZAMOD (the SOUTHMOD tax-benefit model for Zambia, UNU-WIDER / Ministry of Finance and National Planning / ZIPAR, run on the EUROMOD engine) is the parity oracle for this repository. The SOUTHMOD bundle is licensed and non-redistributable: it is referenced by path/sha only, and no bundle bytes, dataset rows, or model XML appear in this repository or its validation artifacts — only comparison statistics and model-produced values.

## Listing gates

This repo carries `app_visibility = "experimental"` in `.axiom/registry.toml` and stays out of app surfaces until:

1. The encoded surface covers the flagship calculation (PAYE gross-to-net for a formal employee) end to end with companion tests.
2. Oracle parity suites exist and pass against MicroZAMOD for the encoded surface.
3. Citation paths are stable (chapter-number vs act-number form resolved against the current Government-Printer edition).
