"""Encoding-manifest state recorded on 2026-10-14.

KNOWN_STALE_ATTESTATIONS lists manifest claims that were already stale. Each
entry is one claim in one manifest under .axiom/encoding-manifests/: the
file it attests, the sha256 the manifest records for that file, the sha256
the file had on 2026-10-14, the sha256 of the manifest file itself, and the
commits that changed the file after it was attested.

All of these changes landed in July 2026 (rulespec-zm#11), while this
repository's generated-RuleSpec guard was off (run-generated-guard: false
until 2026-10-11), so CI never compared the edited files with their
manifests.

The listed manifests are manual attestations (runner: manual-attestation,
schema axiom-encode/applied-rulespec/v1), not encoder apply records. Listing
a claim here records the drift. It does not attest the current bytes, and
the manifest still attests the earlier ones.

KNOWN_UNMANIFESTED_MODULES lists the RuleSpec modules that had no encoding
manifest on 2026-10-14. Any other module without one fails.

Both lists are closed. Every entry must carry a digest in
test_encoding_manifests.py's ADOPTED_LIST_SHA256, so the lists cannot gain
an entry that was not recorded on 2026-10-14; a removed entry could be put
back later, and only review catches that. The test fails if a listed file
changes again, if a listed manifest is edited, removed or retired other than
by an encoder replacement, or if a module loses its manifest. It warns when
an entry resolves, for example once the supervised encoder replaces a
module's manifest; delete the entry then. New drift is fixed through the
encoder, not listed.
"""

from __future__ import annotations

from typing import NamedTuple


class StaleAttestation(NamedTuple):
    manifest: str
    manifest_sha256: str
    path: str
    attested_sha256: str
    current_sha256: str
    changed_by: tuple[str, ...]
    change: str


KNOWN_STALE_ATTESTATIONS: tuple[StaleAttestation, ...] = (
    StaleAttestation(
        manifest=".axiom/encoding-manifests/zm/policies/mcdss-sct/ministerial-statement-transfer-values.json",
        manifest_sha256="378868f43cd04191df841ad461a064bc9079026b5aa40bf36118a978f8a1f495",
        path="zm/policies/mcdss-sct/ministerial-statement-transfer-values.yaml",
        attested_sha256="6c15255020b4fe9f10f81fb7fd44884979459dc2fe5865bc5a03884b480a9bf2",
        current_sha256="6f43ba2bc2ef0bbb05b56bf1a59e11fafec85802f09e29c7796e07707b01d43c",
        changed_by=("1929f8d4d0e659ff268a488ec8bfbcfd39c37677",),
        change=(
            "no formula, parameter or import changed: upstream_source_check "
            "removed, 2 proof excerpts changed"
        ),
    ),
    StaleAttestation(
        manifest=".axiom/encoding-manifests/zm/statutes/act-2023-22/income-tax-amendment-2023.json",
        manifest_sha256="e70c4b28ffd1f6a349a2e3c284246dc16f4508160fe4f8f6c10f564bd347f2db",
        path="zm/statutes/act-2023-22/income-tax-amendment-2023.yaml",
        attested_sha256="82fb0385d2542c9d32b84f0d5fc2d02d674c495bca15eac1f7ea7a4f21256293",
        current_sha256="b3082a382db5bacd139040aaa7e0ada2f2a8d7b1ccedf0592bcaf1367fc39d55",
        changed_by=("1929f8d4d0e659ff268a488ec8bfbcfd39c37677",),
        change=("no formula, parameter or import changed: 2 proof excerpts changed"),
    ),
    StaleAttestation(
        manifest=".axiom/encoding-manifests/zm/statutes/act-2024-24/customs-and-excise-amendment-2024.json",
        manifest_sha256="2bf3d998861d329749da93d53345585bbfcf97187b47e4ca22710f0c9decbd87",
        path="zm/statutes/act-2024-24/customs-and-excise-amendment-2024.yaml",
        attested_sha256="e903dfdc794b02ba00289a90d4ee843fc5aec361f99051b27f2515808628916f",
        current_sha256="d030d74351230939adb446f1e9a62793507ec9c3eb5a4e48c74684642045241a",
        changed_by=("1929f8d4d0e659ff268a488ec8bfbcfd39c37677",),
        change=(
            "four duty-rate parameters moved out to imports from "
            "zm:statutes/act-2018-19/customs-and-excise-amendment-2018 and "
            "zm:statutes/act-2021-45/customs-and-excise-amendment-2021, which "
            "have no manifests; same values and effective dates; one deferred "
            "output added; also module citation list collapsed to one "
            "corpus_citation_path, upstream_source_check removed, 7 proof "
            "excerpts changed, 7 proof citations changed, 4 rule source labels "
            "changed"
        ),
    ),
    StaleAttestation(
        manifest=".axiom/encoding-manifests/zm/statutes/cap-331/value-added-tax-act.json",
        manifest_sha256="12b745c4b19f4bcd91647605b80b86d9581d7b70cc1390763bebd17219c9f5bf",
        path="zm/statutes/cap-331/value-added-tax-act.yaml",
        attested_sha256="065e68d3fb2a50bbd8504714c1b08bb968fa509d4a9f23d3d755ca7077a7be85",
        current_sha256="5b12c9fae799933c8b678fb4ae24b777d19cca197d0681e5a2dc97f2ff31fc7f",
        changed_by=("1929f8d4d0e659ff268a488ec8bfbcfd39c37677",),
        change=(
            "no formula, parameter or import changed: module citation list "
            "collapsed to one corpus_citation_path, upstream_source_check "
            "removed"
        ),
    ),
    StaleAttestation(
        manifest=".axiom/encoding-manifests/zm/statutes/composed/pilot-worker-disposable-income-pipeline.json",
        manifest_sha256="31e56d2137eb42fed01f7aa6a60c93185c682b3d5a6e7ae6e75e4625d46bdd44",
        path="zm/statutes/composed/pilot-worker-disposable-income-pipeline.yaml",
        attested_sha256="d089f690708d93efd6301d58214715da0821a30c0934784bc1b471fd9039c530",
        current_sha256="3f9de7626a92185addc30afc5c6137369ed39623f6a489374784ac5215977a8a",
        changed_by=("1929f8d4d0e659ff268a488ec8bfbcfd39c37677",),
        change=(
            "no formula, parameter or import changed: module citation list "
            "collapsed to one corpus_citation_path, upstream_source_check "
            "removed"
        ),
    ),
)

KNOWN_UNMANIFESTED_MODULES: tuple[str, ...] = (
    "zm/policies/zra-pn-2008-1/vat-rate-of-tax-order-16-percent.yaml",
    "zm/policies/zra-pn-2024-1/clear-beer-suspension-regulations.yaml",
    "zm/regulations/si-2025-103/pensionable-earnings-amendment-2025.yaml",
    "zm/statutes/act-2018-19/customs-and-excise-amendment-2018.yaml",
    "zm/statutes/act-2021-45/customs-and-excise-amendment-2021.yaml",
    "zm/statutes/act-2023-1/national-pension-scheme-amendment-2023.yaml",
    "zm/statutes/act-2023-25/customs-and-excise-amendment-2023.yaml",
    "zm/statutes/cap-256/national-pension-scheme-act.yaml",
)
