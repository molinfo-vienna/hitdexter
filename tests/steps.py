from pytest_bdd import given

from hitdexter import HitDexter3Model


@given("the HitDexter 3 model", target_fixture="model")
def hitdexter3_model():
    return HitDexter3Model()
