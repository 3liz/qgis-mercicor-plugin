__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

type_pression__pression = {
    'id': 'type_pression-pression',
    'name': 'Type pression - Pression',
    'referenced_layer': 'liste_type_pression',
    'referenced_field': 'key',
    'referencing_layer': 'pression',
    'referencing_field': 'type_pression',
}

scenario_pression__pression = {
    'id': 'scenario_pression-pression',
    'name': 'Scénario pression - Pression',
    'referenced_layer': 'scenario_pression',
    'referenced_field': 'id',
    'referencing_layer': 'pression',
    'referencing_field': 'scenario_id',
}

scenario_pression__habitat_pression_etat_ecologique = {
    'id': 'scenario_pression-habitat_pression_etat_ecologique',
    'name': 'Scénario pression - Habitat pression état écologique',
    'referenced_layer': 'scenario_pression',
    'referenced_field': 'id',
    'referencing_layer': 'habitat_pression_etat_ecologique',
    'referencing_field': 'scenario_id',
}

habitat__habitat_etat_ecologique = {
    'id': 'habitat-habitat_etat_ecologique',
    'name': 'Habitat état écologique - Habitat',
    'referenced_layer': 'habitat_etat_ecologique',
    'referenced_field': 'id',
    'referencing_layer': 'habitat',
    'referencing_field': 'id',
}

habitat_pression_etat_ecologique__habitat = {
    'id': 'habitat_pression_etat_ecologique-habitat',
    'name': 'Habitat pression état écologique - Habitat',
    'referenced_layer': 'habitat_pression_etat_ecologique',
    'referenced_field': 'habitat_id',
    'referencing_layer': 'habitat',
    'referencing_field': 'id',
}

pression_habitat_pression_etat_ecologique__pression = {
    'id': 'pression_habitat_pression_etat_ecologique-pression',
    'name': 'Habitat pression état écologique - Pression',
    'referenced_layer': 'habitat_pression_etat_ecologique',
    'referenced_field': 'pression_id',
    'referencing_layer': 'pression',
    'referencing_field': 'id',
}

relations = [
    type_pression__pression,
    scenario_pression__pression,
    scenario_pression__habitat_pression_etat_ecologique,
    habitat__habitat_etat_ecologique,
    habitat_pression_etat_ecologique__habitat,
    pression_habitat_pression_etat_ecologique__pression,
]
