from pytest_bdd import parsers, when

from hitdexter import HitDexter3Model


@when(
    parsers.parse(
        "the HitDexter 3 model generates predictions for the molecule representations"
    ),
    target_fixture="predictions",
)
def predictions(representations, input_type):
    model = HitDexter3Model()
    return model.predict(
        representations,
        input_type=input_type,
        output_format="record_list",
    )
