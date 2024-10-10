@hitdexter
Feature: Valid predictions

  Scenario Outline: Predictions are valid
    Given a random seed set to <seed>
    And the input type is '<input_type>'
    And a list of <num_molecules> random molecules, where <num_none> entries are None
    And the representations of the molecules
    And the HitDexter 3 model

    When the model generates predictions for the molecule representations
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
            patterns_1
            patterns_2
            patterns_3
            patterns_4
            patterns_5
            patterns_6
            patterns_7
            patterns_8
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
    And the value in column 'patterns_1' should have type 'list'
    And the value in column 'patterns_2' should have type 'list'
    And the value in column 'patterns_3' should have type 'list'
    And the value in column 'patterns_4' should have type 'list'
    And the value in column 'patterns_5' should have type 'list'
    And the value in column 'patterns_6' should have type 'list'
    And the value in column 'patterns_7' should have type 'list'
    And the value in column 'patterns_8' should have type 'list'


  Examples:
  | seed | num_molecules | num_none | input_type |
  | 1    | 10            | 0        | smiles     |
  | 2    | 10            | 1        | smiles     |
  | 3    | 10            | 2        | smiles     |
  | 4    | 10            | 10       | smiles     |
