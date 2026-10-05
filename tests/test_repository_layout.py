from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
JURISDICTION_DIR_RE = re.compile(r"^[a-z]{2}(-[a-z0-9-]+)*$")
CONTENT_DIRS = ("statutes", "regulations", "policies", "legislation")
IGNORED_DIRS = {".git", ".pytest_cache", ".ruff_cache", ".venv", "__pycache__"}
ALLOWED_ROOT_DIRS = {".axiom", ".github", "bulk", "data", "programs", "tests", "zm"}
ALLOWED_ROOT_FILES = {
    ".gitignore",
    "CLAUDE.md",
    "LICENSE",
    "LICENSE-CODE",
    "NOTICE",
    "README.md",
    "known-missing-money-atoms.yaml",
    "known-validation-gaps.yaml",
    "oracle-coverage-pending.yaml",
    "variables.toml",
}


def jurisdiction_dirs() -> list[Path]:
    return sorted(
        child
        for child in ROOT.iterdir()
        if child.is_dir()
        and JURISDICTION_DIR_RE.match(child.name)
        and any((child / marker).is_dir() for marker in CONTENT_DIRS)
    )


def rulespec_content_roots() -> list[Path]:
    return [
        jurisdiction / marker
        for jurisdiction in jurisdiction_dirs()
        for marker in CONTENT_DIRS
        if (jurisdiction / marker).is_dir()
    ]


def iter_rulespec_files() -> list[Path]:
    files: list[Path] = []
    for root in rulespec_content_roots():
        files.extend(
            path
            for path in root.rglob("*.yaml")
            if not path.name.endswith(".test.yaml")
        )
    return sorted(files)


def test_only_zambia_namespace_present() -> None:
    """Zambia is unitary: the only jurisdiction directory is zm/."""
    names = {d.name for d in jurisdiction_dirs()}
    assert names <= {"zm"}, f"unexpected jurisdiction dirs: {names - {'zm'}}"


def test_zm_content_buckets_exist() -> None:
    for marker in ("statutes", "regulations", "policies"):
        assert (ROOT / "zm" / marker).is_dir(), f"missing zm/{marker}"


def test_root_directories_are_allowed() -> None:
    # The org validate-rulespec workflow checks out sibling toolchain repos
    # (axiom-encode, axiom-rules-engine, ...) into a `_axiom/` directory and
    # skips any `_`- or `.`-prefixed directory during shard discovery. Mirror
    # that: ignore underscore/dot-prefixed dirs so CI's transient checkouts do
    # not trip the layout gate.
    found = {
        child.name
        for child in ROOT.iterdir()
        if child.is_dir()
        and child.name not in IGNORED_DIRS
        and not child.name.startswith(("_", "."))
    }
    unexpected = found - ALLOWED_ROOT_DIRS
    assert not unexpected, f"unexpected root directories: {unexpected}"


def test_root_files_are_allowed() -> None:
    # In a git worktree checkout `.git` is a gitdir-pointer file rather than
    # a directory, so exclude it here just as IGNORED_DIRS excludes the
    # `.git` directory in normal clones.
    found = {
        child.name
        for child in ROOT.iterdir()
        if child.is_file() and child.name != ".git"
    }
    unexpected = found - ALLOWED_ROOT_FILES
    assert not unexpected, f"unexpected root files: {unexpected}"


def test_every_rulespec_has_companion_test() -> None:
    """Any encoded rule module must ship a companion .test.yaml alongside it."""
    for path in iter_rulespec_files():
        companion = path.with_name(path.name[: -len(".yaml")] + ".test.yaml")
        assert companion.exists(), f"{path} is missing companion {companion.name}"


def test_money_atom_ratchet_is_nonnegative_int() -> None:
    payload = yaml.safe_load((ROOT / "known-missing-money-atoms.yaml").read_text())
    allowed = payload["total_allowed"]
    assert isinstance(allowed, int) and allowed >= 0


ORACLE_INDEX = ROOT / "data/oracles/oracle-index.json"
SOURCE_MAP = ROOT / "data/coverage/tax-benefit-source-map.json"
SYSTEM_RE = re.compile(r"\b([A-Z]{2})_\d{4}\b")
# The other SOUTHMOD country models: (country code, model id, model name,
# country). None of them may appear in this repository's oracle data.
OTHER_SOUTHMOD_MODELS = (
    ("gh", "ghamod", "GHAMOD", "Ghana"),
    ("ug", "ugamod", "UGAMOD", "Uganda"),
    ("rw", "rwamod", "RWAMOD", "Rwanda"),
    ("et", "etmod", "ETMOD", "Ethiopia"),
    ("tz", "tazmod", "TAZMOD", "Tanzania"),
    ("mz", "mozmod", "MOZMOD", "Mozambique"),
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def microzamod_entry() -> dict:
    oracles = load_json(ORACLE_INDEX)["oracles"]
    assert len(oracles) == 1, "expected exactly one oracle (MicroZAMOD)"
    return oracles[0]


def iter_strings(value, key: str = ""):
    """Yield (key, string) for every string value in a JSON tree."""
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from iter_strings(child, child_key)
    elif isinstance(value, list):
        for child in value:
            yield from iter_strings(child, key)
    elif isinstance(value, str):
        yield key, value


def encoded_modules() -> set[str]:
    """Repo-relative paths of encoded RuleSpec modules.

    iter_rulespec_files walks only the content buckets, so the compose spec
    under zm/programs/ is not a module here.
    """
    return {path.relative_to(ROOT).as_posix() for path in iter_rulespec_files()}


def test_oracle_index_identifies_microzamod() -> None:
    payload = load_json(ORACLE_INDEX)
    assert payload["jurisdiction"] == "zm"
    entry = microzamod_entry()
    assert entry["id"] == "microzamod"
    assert entry["name"] == "MicroZAMOD"
    assert entry["url"].startswith("https://www.wider.unu.edu/about/")
    assert "microzamod" in entry["url"]
    assert entry["authority"] == "wired_per_case_parity"
    assert entry["availability_check"]["status"] == "wired_per_case_parity"


def test_oracle_index_systems_are_zambian() -> None:
    entry = microzamod_entry()
    wired = entry["wired"]
    system_strings = [entry["systems"], wired["system"]]
    system_strings += [
        suite["system"] for suite in wired["suites"] if "system" in suite
    ]
    for text in system_strings:
        prefixes = SYSTEM_RE.findall(text)
        assert prefixes, f"no system identifier in {text!r}"
        assert set(prefixes) == {"ZM"}, f"non-Zambian system in {text!r}"
    assert re.fullmatch(r"ZM_\d{4}", wired["system"])
    assert wired["dataset_configuration"].startswith("zm_")


def test_oracle_index_suite_statistics_add_up() -> None:
    wired = microzamod_entry()["wired"]
    suites = wired["suites"]
    assert suites, "wired block lists no suites"
    for suite in suites:
        name = suite["suite"]
        assert name.startswith("zm-"), name
        assert suite["matched"] + suite["dispositioned"] == suite["comparisons"], name
        assert len(suite["axiom_outputs"]) == len(suite["microzamod_variables"]), name
    assert len({suite["suite"] for suite in suites}) == len(suites)
    totals = {"suites": len(suites)}
    for field in ("cases", "comparisons", "matched", "dispositioned"):
        totals[field] = sum(suite[field] for suite in suites)
    assert wired["totals"] == totals


def test_oracle_index_outputs_resolve_to_modules() -> None:
    for suite in microzamod_entry()["wired"]["suites"]:
        for output in suite["axiom_outputs"]:
            match = re.fullmatch(r"zm:([a-z0-9/_-]+)#([a-z0-9_]+)", output)
            assert match, f"{suite['suite']}: malformed output {output}"
            path, name = match.groups()
            module = ROOT / "zm" / f"{path}.yaml"
            assert module.is_file(), f"{suite['suite']}: no module zm/{path}.yaml"
            payload = yaml.safe_load(module.read_text())
            rules = {rule["name"] for rule in payload.get("rules") or []}
            assert name in rules, f"{suite['suite']}: zm/{path}.yaml defines no {name}"


def test_oracle_index_records_no_local_paths() -> None:
    # Only the local_path field may name the licensed bundle's location.
    for key, text in iter_strings(load_json(ORACLE_INDEX)):
        if key == "local_path":
            continue
        assert "~/" not in text and "/Users/" not in text, f"local path in {key}"
    detail = microzamod_entry()["availability_check"]["detail"]
    assert "~/" not in detail and "/Users/" not in detail


def test_source_map_tracks_resolve() -> None:
    payload = load_json(SOURCE_MAP)
    assert payload["jurisdiction"] == "zm"
    suites = {suite["suite"] for suite in microzamod_entry()["wired"]["suites"]}
    for track in payload["tracks"]:
        modules = track.get("rulespec_modules", [])
        assert (track["status"] == "encoded") == bool(modules), track["id"]
        for module in modules:
            assert (ROOT / module).is_file(), f"{track['id']}: missing {module}"
        for suite in track.get("oracle_suites", []):
            assert suite in suites, f"{track['id']}: unknown oracle suite {suite}"


def test_source_map_covers_every_encoded_module() -> None:
    tracked = {
        module
        for track in load_json(SOURCE_MAP)["tracks"]
        for module in track.get("rulespec_modules", [])
    }
    untracked = encoded_modules() - tracked
    assert not untracked, (
        f"encoded modules missing from the source map: {sorted(untracked)}"
    )


def test_oracle_data_names_no_other_southmod_country() -> None:
    for path in (ORACLE_INDEX, SOURCE_MAP):
        text = path.read_text()
        lowered = text.lower()
        for code, model_id, model_name, country in OTHER_SOUTHMOD_MODELS:
            where = path.relative_to(ROOT)
            assert model_id not in lowered, f"{where} names {model_name}"
            assert country.lower() not in lowered, f"{where} names {country}"
            assert code.upper() not in SYSTEM_RE.findall(text), (
                f"{where} names a {code.upper()}_YYYY system"
            )


def test_toolchain_pins_are_full_shas() -> None:
    import tomllib

    payload = tomllib.loads((ROOT / ".axiom/toolchain.toml").read_text())
    toolchain = payload["toolchain"]
    assert set(toolchain) == {
        "axiom_corpus_release",
        "axiom_corpus_release_content_sha256",
        "validation_waiver_set_sha256",
    }
    assert re.fullmatch(
        r"[a-z]{2}-rulespec-\d{4}-\d{2}-\d{2}", toolchain["axiom_corpus_release"]
    ), "release must be an immutable dated name"
    sha256_re = re.compile(r"^[0-9a-f]{64}$")
    assert sha256_re.match(toolchain["axiom_corpus_release_content_sha256"])
    assert sha256_re.match(toolchain["validation_waiver_set_sha256"])
