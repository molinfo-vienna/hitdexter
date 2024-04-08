from rdkit.Chem import MolFromSmarts


def match_smarts_patterns_to_mol(patterns, mol):
    """
    Method for doing rdkit substructure search for mol with the patterns

    .. note::
       the addHs of rdkit have to be done on the molecule to find all matches

    :param patterns: SMART patterns
    :param mol: molecule for that substruces should be found
    :return: list of matches
    """
    result = []
    for smart in patterns:
        if mol.HasSubstructMatch(MolFromSmarts(smart)):
            result.append(smart)
    return result
