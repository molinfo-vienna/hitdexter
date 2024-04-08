import sys

from rdkit import Chem

if sys.version_info < (3, 9):
    from importlib_resources import files
else:
    from importlib.resources import files

rule_set_files = [
    "bms",
    "chakravorty_extreme_caution",
    "chakravorty",
    "cypsmarts",
    "dundee",
    "glaxo_reactives",
    "glaxo",
    "inpharmatica",
    "lint",
    "merck",
    "mlsmr",
    "ncypsmarts",
    "pains",
    "sure_chembl",
]

rule_set_names = [f"{rule_set}_patterns" for rule_set in rule_set_files]


__all__ = rule_set_names + ["rule_set_names"]

for rule_set in rule_set_files:
    f = files("hitdexter").joinpath(f"patterns/{rule_set}.smarts").open()
    patterns = f.read().splitlines()

    # remove trailing commas, newlines and whitespace
    patterns = [p.strip(" ,\n") for p in patterns]

    # remove comments
    patterns = [p for p in patterns if not p.startswith("#")]

    # remove empty lines
    patterns = [p for p in patterns if p != ""]

    # create dictionary where
    # key = SMARTS pattern as string
    # value = SMARTS pattern as rdkit mol object
    pattern_mapping = {pattern: Chem.MolFromSmarts(pattern) for pattern in patterns}

    # let this dictionary be a module attribute with the name of the rule set
    # e.g. bms_patterns for the rule_set 'bms'
    globals()[f"{rule_set}_patterns"] = pattern_mapping
