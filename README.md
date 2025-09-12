# Hit-Dexter

## Installation

```bash
conda env create -f environment.yml

conda activate hitdexter

# fix a problem with the RDKit installation (keeping pip from seeing the conda-installed RDKit)
curl -sS https://gist.githubusercontent.com/shirte/e1734e51dbc72984b2d918a71b68c25b/raw/ae4afece11980f5d7da9e7668a651abe349c357a/rdkit_installation_fix.sh | bash -s hitdexter

pip install .
```

## Contribute

```
conda env create -f environment.yml
conda activate hitdexter
pip install -e .[dev,test]
ptw
```