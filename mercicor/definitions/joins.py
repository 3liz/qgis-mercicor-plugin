__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

joins = [
    {
        'join_field_name': 'id',
        'target_field_name': 'id',
        'join_layer': 'habitat_etat_ecologique',
        'layer_add_join': 'habitat',
        'prefix': '',
    },
    {
        'join_field_name': 'id',
        'target_field_name': 'habitat_id',
        'join_layer': 'habitat',
        'layer_add_join': 'habitat_pression_etat_ecologique',
        'prefix': 'hab_'
    },
    {
        'join_field_name': 'id',
        'target_field_name': 'pression_id',
        'join_layer': 'pression',
        'layer_add_join': 'habitat_pression_etat_ecologique',
        'prefix': 'pression_',
    },
    {
        'join_field_name': 'id',
        'target_field_name': 'scenario_id',
        'join_layer': 'scenario_pression',
        'layer_add_join': 'habitat_pression_etat_ecologique',
        'prefix': 'scenario_',
    },
]
