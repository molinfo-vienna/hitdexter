from nerdd_module import auto_cli

from .hitdexter3_model import HitDexter3Model


@auto_cli
def main():
    return HitDexter3Model()
