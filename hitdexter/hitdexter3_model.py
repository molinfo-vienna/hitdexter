import sys
from typing import List

import numpy as np
import pandas as pd
from FPSim2 import FPSim2Engine
from joblib import load
from nerdd_module import AbstractModel
from rdkit.Chem import AllChem, Mol, MolToSmiles
from rdkit.Chem.Crippen import MolLogP
from rdkit.Chem.Descriptors import MolWt
from rdkit.Chem.rdmolops import AddHs

from .patterns import hitdexter_patterns, match_smarts_patterns_to_mol
from .preprocessing import HitdexterPreprocessingPipeline

if sys.version_info < (3, 9):
    from importlib_resources import files
else:
    from importlib.resources import files

__all__ = ["HitDexter3Model"]

labels = [
    "TARGET_HN",
    "TARGET_MN",
    "SCELL_HN",
    "SCELL_MN",
    "ACELL_HN",
    "ACELL_MN",
]


def load_ml_nn_models(labels):
    ml_data = []
    nn_data = []

    for i in range(len(labels)):
        ml_data.append(
            load(
                files("hitdexter").joinpath(
                    "models/ml_models/" + labels[i] + "_MultiCore.pkl"
                )
            )
        )
        nn_data.append(
            FPSim2Engine(
                str(
                    files("hitdexter").joinpath("models/nn_models/" + labels[i] + ".h5")
                )
            )
        )

    return ml_data, nn_data


mlm, nnm = load_ml_nn_models(labels)


def get_mol_with_added_hs(mol):
    """
    Method to addHs to molecules

    :param mol: rdkit molecule
    :return: rdkits AddHs(mol)
    """
    return AddHs(mol)


def get_morgan2_fp(mol):
    """
    Method to calculate morgan2Fps

    :param mol: rdkit molecule
    :return: rdkits GetMorganFingerprintAsBitVect(mol,2,1024) (Morgan2FP)
    """
    return AllChem.GetMorganFingerprintAsBitVect(mol, 2, 1024)


def get_rounded_molWt(mol):
    """
    Method to calculated rounded molecule weight

    :param mol: rdkit molecule
    :return: rounded molecule weight from rdkit MolWt(mol)
    """
    return round(MolWt(mol), 2)


def get_rounded_molLogP(mol):
    """
    Method to calculated rounded LogP

    :param mol: rdkit molecule
    :return: rounded molecule LogP from rdkit MolLogP(mol)
    """
    return round(MolLogP(mol), 2)


def get_machine_learning_prediction(model, morgans):
    """
    Method to get the rounded predictions of the models

    :param model: Machine learning model
    :param morgans: list Morgan2FP for query
    :return: rounded predictions of model for morgans
    """
    if len(morgans) == 0:
        return []

    prediction = model.predict_proba(morgans)[:, 1]

    return [round(i, 2) for i in prediction]


def get_nearest_neighbors_scores(model, mols):
    """
    Method to get the distance to closest training instance

    :param model: Machine learning model
    :param mols: list of molecules
    :return: nearest neighbor score of model for smiles
    """
    arr_size = len(mols)
    scores = np.empty(arr_size)
    similarity = []

    for i in range(arr_size):
        try:
            similarity = model.similarity(MolToSmiles(mols[i]), 0.0, n_workers=1)
        except:
            pass
        if len(similarity) != 0:
            scores[i] = np.round(1.0 - similarity[0][1], 2)
        else:
            scores[i] = 1.0

    return scores


def get_matching_hitdexter3_patterns(mol):
    """
    Method to match smart hitdexter SMART patterns against query

    :param mol: rdkit molecule
    :return: list of matched patterns
    """
    matchedList = [
        match_smarts_patterns_to_mol(hitdexter_patterns[pat], mol)
        for pat in hitdexter_patterns
    ]
    return matchedList


def produce_hitdexter3_comment(args):
    """
    Method that creates the hitdexter3 comment for the comment column

    :param predictions (args[0]): list of predictions in form of hpTB,mpTB,hpCB,mpCB,hpECB,mpECB
    :param similaritys (args[1]): list of similarities of the compounds with respect to the dataset
    :return: the built comment
    """
    predictions, similarity = args
    comment = ""
    # Text
    start = "* Predicted as"
    middle = " with a probability of {:.2f}"
    end = "\n"
    # Promiscuity
    mp = " promiscuous"
    np = " non-promiscuous"
    hp = " highly-promiscuous"
    # Classifiers
    tb = " by the target-based assay data set classifier"
    cb = " by the cell-based assay data set classifier"
    ecb = " by the extended cell-based assay data set classifier"
    # Build phrase
    for i, value in enumerate(predictions):
        # Get confidence:
        conf = get_confidence_for_similarity(similarity[i])
        # Get classfier and promicuity level
        # Cutoff 0.5 for (highly-)promiscuous or non-promiscous
        if value >= 0.5:
            # In case of 0 and 2 predicted as highly-promiscous
            if i % 2 == 0:
                # First 2 elements are with respect to the TB classifier
                if i < 2:
                    clf = tb
                # Second 2 elements are with respect to the CB classifier
                elif i >= 2 and i < 4:
                    clf = cb
                # Third 2 elements are with respect to the ECB classifier
                elif i >= 4:
                    clf = ecb
                comment += start + hp + clf + middle.format(value) + conf + end
            # In case of 1 and 3 predicted as promiscous
            elif i % 2 == 1:
                # First 2 elements are with respect to the TB classifier
                if i < 2:
                    clf = tb
                # Second 2 elements are with respect to the CB classifier
                elif i >= 2 and i < 4:
                    clf = cb
                # Third 2 elements are with respect to the ECB classifier
                elif i >= 4:
                    clf = ecb
                comment += start + mp + clf + middle.format(value) + conf + end
        # Cutoff 0.5 for (highly-)promiscuous or non-promiscous
        # In all cases predicted as non-promiscous
        elif value < 0.5:
            # First 2 elements are with respect to the TB classifier
            if i < 2:
                clf = tb
            # Second 2 elements are with respect to the CB classifier
            elif i >= 2 and i < 4:
                clf = cb
            # Third 2 elements are with respect to the ECB classifier
            elif i >= 4:
                clf = ecb
            comment += start + np + clf + middle.format(1 - value) + conf + end
    return comment


def get_confidence_for_similarity(similarity):
    """
    Method that returns the confidence for a given similarity

    :param similarity: Similarity to training set
    :return: confidence
    """
    high_confidence = " at high confidence"
    low_confidence = " at low confidence"
    moderate_confidence = " at moderate confidence"
    no_confidence = " with no confidence (similarity turned off)"
    if similarity >= 0.8:
        return high_confidence
    elif similarity == -1:
        return no_confidence
    elif similarity < 0.5:
        return low_confidence
    elif similarity < 0.8:
        return moderate_confidence


def predict(
    mols,
):
    # calculate features
    mols_h = [get_mol_with_added_hs(m) for m in mols]
    morgans = [get_morgan2_fp(m) for m in mols]
    mol_wts = [get_rounded_molWt(m) for m in mols_h]
    mol_logps = [get_rounded_molLogP(m) for m in mols_h]

    mlm_predictions = [
        get_machine_learning_prediction(mlmodel, morgans) for mlmodel in mlm
    ]

    nnm_predictions = [get_nearest_neighbors_scores(nnmodel, mols) for nnmodel in nnm]

    pattern_list = [get_matching_hitdexter3_patterns(m) for m in mols_h]

    comments = [
        produce_hitdexter3_comment((entry, entry)) for entry in zip(*mlm_predictions)
    ]

    results = pd.DataFrame(
        dict(
            assessment=comments,
            mol_weight=mol_wts,
            mol_clogp=mol_logps,
        )
    )

    for i in range(len(labels)):
        results[f"prediction_{i+1}"] = mlm_predictions[i]
        results[f"neighbor_{i+1}"] = nnm_predictions[i]

    for i in range(len(hitdexter_patterns)):
        results[f"pattern_{i+1}"] = [j[i] if j else None for j in pattern_list]

    return results


class HitDexter3Model(AbstractModel):
    def __init__(self):
        super().__init__(
            preprocessing_pipeline=HitdexterPreprocessingPipeline(),
        )

    def _predict_mols(self, mols: List[Mol]) -> pd.DataFrame:
        return predict(mols)
