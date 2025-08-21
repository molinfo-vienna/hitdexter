@hitdexter
Feature: Valid predictions

  Scenario Outline: Predictions are valid
    Given a random seed set to <seed>
    And a list of <num_molecules> random molecules, where 
        * <num_none> entries are None
        * each mol has a weight between 180 and 900
    And the representations of the molecules in <input_type> format

    When the HitDexter 3 model generates predictions for the molecule representations
    And the subset of the result where the input was not None is considered

    Then the result should contain the columns:
            assessment
            mol_weight
            mol_clogp
            prediction_1
            distance_to_neighbor_1
            prediction_2
            distance_to_neighbor_2
            prediction_3
            distance_to_neighbor_3
            prediction_4
            distance_to_neighbor_4
            prediction_5
            distance_to_neighbor_5
            prediction_6
            distance_to_neighbor_6
            pains
            bms
            dundee
            glaxo
            lint
            mlsmr
            sure_chembl
            chakravorty
    And the value in column 'assessment' should have type 'str'
    And the value in column 'assessment' should have length greater than 0
    And the value in column 'mol_weight' should have type 'float'
    And the value in column 'mol_weight' should be between 0 and infinity
    And the value in column 'mol_clogp' should have type 'float'
    And the value in column 'prediction_1' should be between 0 and 1
    And the value in column 'distance_to_neighbor_1' should be between 0 and 1
    And the value in column 'prediction_2' should be between 0 and 1
    And the value in column 'distance_to_neighbor_2' should be between 0 and 1
    And the value in column 'prediction_3' should be between 0 and 1
    And the value in column 'distance_to_neighbor_3' should be between 0 and 1
    And the value in column 'prediction_4' should be between 0 and 1
    And the value in column 'distance_to_neighbor_4' should be between 0 and 1
    And the value in column 'prediction_5' should be between 0 and 1
    And the value in column 'distance_to_neighbor_5' should be between 0 and 1
    And the value in column 'prediction_6' should be between 0 and 1
    And the value in column 'distance_to_neighbor_6' should be between 0 and 1
    And the value in column 'pains' should have type 'list'
    And the value in column 'bms' should have type 'list'
    And the value in column 'dundee' should have type 'list'
    And the value in column 'glaxo' should have type 'list'
    And the value in column 'lint' should have type 'list'
    And the value in column 'mlsmr' should have type 'list'
    And the value in column 'sure_chembl' should have type 'list'
    And the value in column 'chakravorty' should have type 'list'


  Examples:
  | seed | num_molecules | num_none | input_type |
  | 1    | 10            | 0        | smiles     |
  | 2    | 10            | 1        | smiles     |
  | 3    | 10            | 2        | smiles     |
  | 4    | 10            | 10       | smiles     |
