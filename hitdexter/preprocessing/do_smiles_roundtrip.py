from typing import List, Tuple

from nerdd_module import Problem
from nerdd_module.preprocessing import PreprocessingStep
from rdkit.Chem import CanonSmiles, Mol, MolFromSmiles, MolToSmiles


class DoSmilesRoundtrip(PreprocessingStep):
    def __init__(self, remove_stereo: bool = True):
        super().__init__()
        self.remove_stereo = remove_stereo

    def _preprocess(self, mol: Mol) -> Tuple[Mol, List[Problem]]:
        errors = []
        smiles = MolToSmiles(mol, True)
        if self.remove_stereo:
            smiles = CanonSmiles(smiles, useChiral=0)
        mol = MolFromSmiles(smiles)

        if mol is None:
            errors.append("V1")

        return mol, errors
