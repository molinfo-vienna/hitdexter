from pytest_bdd import given, parsers, when

from hitdexter import HitDexter3Model


@given("the HitDexter 3 model", target_fixture="predictor")
def hitdexter3_model():
    return HitDexter3Model()


@when(
    parsers.parse("the model generates predictions for the molecule representations"),
    target_fixture="predictions",
)
def predictions(representations, predictor, input_type):
    return predictor.predict(
        representations,
        input_type=input_type,
        output_format="record_list",
    )