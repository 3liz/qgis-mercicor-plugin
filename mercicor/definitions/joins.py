__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

# layer_add_join is the layer on which we want to add the join.
# join_layer is the target

attribute_joins = [
    {
        'join_field_name': 'id',
        'target_field_name': 'id',
        'join_layer': 'habitat_etat_ecologique',
        'layer_add_join': 'habitat',
        'prefix': '',
        'block_list': ['nom', 'facies']
    },
]

attribute_joins_pression = [
    {
        'join_field_name': 'id',
        'target_field_name': 'habitat_id',
        'join_layer': 'habitat_etat_ecologique',
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
attribute_joins_pression.extend(attribute_joins)

attribute_joins_compensation = [
    {
        'join_field_name': 'id',
        'target_field_name': 'habitat_id',
        'join_layer': 'habitat_etat_ecologique',
        'layer_add_join': 'habitat_compensation_etat_ecologique',
        'prefix': 'hab_'
    },
    {
        'join_field_name': 'id',
        'target_field_name': 'compensation_id',
        'join_layer': 'compensation',
        'layer_add_join': 'habitat_compensation_etat_ecologique',
        'prefix': 'compensation_',
    },
    {
        'join_field_name': 'id',
        'target_field_name': 'scenario_id',
        'join_layer': 'scenario_compensation',
        'layer_add_join': 'habitat_compensation_etat_ecologique',
        'prefix': 'scenario_',
    },
]
attribute_joins_compensation.extend(attribute_joins)

spatial_joins = [
    {
        'input': 'habitat',
        'target': 'observations',
    },
]
