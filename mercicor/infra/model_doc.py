#!/usr/bin/env python3
import os

from os.path import join

from qgis.PyQt.QtCore import QVariant

from mercicor.definitions.joins import spatial_joins
from mercicor.definitions.relations import relations
from mercicor.definitions.tables import tables
from mercicor.qgis_plugin_tools import load_csv, resources_path

PATH = '/model'

TEMPLATE = '''---
hide:
  - navigation
---

# Modèle de données

## Relations

??? info "Légende"
    Flèche pleine : relation de projet

    Losange vide : jointure spatiale

{relationships}

## Tables

??? info "Légende"
    Champ géométrique en *italique*

    Champ de clé primaire en **gras**

    Champ de clé étrangère cliquable avec la mention "FK"

'''

TEMPLATE_TABLE = '''### {name}

| ID | Name | Type | Alias |
|:-:|:-:|:-:|:-:|
{fields}
'''

TEMPLATE_FIELDS = '|{id}|{name}|{type}|{alias}|\n'

TEMPLATE_MERMAID = '''\'\'\'classDiagram
\'\'\'
'''


def slug(table):
    return table.replace('_', '-')


def find_relation(field_name, table):
    for relation in relations:
        if relation['referencing_layer'] == table and relation['referencing_field'] == field_name:
            return relation['referenced_layer']
        elif relation['referenced_layer'] == table and relation['referenced_field'] == field_name:
            return relation['referencing_layer']

def generate_model_doc():  # NOQA C901
    global TEMPLATE

    markdown_all = TEMPLATE

    files = os.listdir(resources_path('data_models'))
    mermaid_md = '```mermaid\n'
    mermaid_md += 'classDiagram\n'

    mermaid_field_md = ''

    for csv_file in files:
        table_name = csv_file.replace('.csv', '')

        if table_name == 'metadata':
            continue

        md = ''

        # Ajout de la geom
        if tables[table_name] != 'None':
            field_md = TEMPLATE_FIELDS.format(
                id='',
                name='*geom*',
                type=tables[table_name],
                alias='',
            )
            md += field_md
            mermaid_field_md += '{} : geom {}\n'.format(
                table_name,
                tables[table_name],
            )

        mermaid_md += table_name + '\n'
        pretty_name = table_name.replace('_', ' ')
        pretty_name = pretty_name.title()
        csv = load_csv(csv_file, resources_path('data_models', csv_file))

        for i, field in enumerate(csv.getFeatures()):

            display_name = mermaid_display_name = field['name']

            if display_name == 'id':
                display_name = '**' + display_name + '**'
                mermaid_display_name += ' PK'

            if display_name.endswith('_id'):
                display_name = '[{title} FK](#{anchor})'.format(
                    title=display_name,
                    anchor=slug(find_relation(field['name'], table_name))
                )
                mermaid_display_name += ' FK'

            field_md = TEMPLATE_FIELDS.format(
                id=field['idx'],
                name=display_name,
                type=QVariant.typeToName(int(field['type'])),
                alias=field['alias'],
            )
            md += field_md

            if i < 10:
                mermaid_field_md += '{} : {}\n'.format(
                    table_name,
                    mermaid_display_name,
                )
            elif i == 10:
                mermaid_field_md += '{} : ...\n'.format(table_name)

        markdown = TEMPLATE_TABLE.format(name=pretty_name, fields=md)
        markdown_all += markdown

    for relation in relations:
        mermaid_md += '{} <|-- {}\n'.format(
            relation['referenced_layer'],
            relation['referencing_layer'],
        )

    for spatial_join in spatial_joins:
        mermaid_md += '{} o-- {}\n'.format(
            spatial_join['input'],
            spatial_join['target'],
        )

    mermaid_md += mermaid_field_md
    mermaid_md += '```'
    markdown_all = markdown_all.format(relationships=mermaid_md)

    output_file = join(PATH, 'README.md')
    output_file = '/home/etienne/dev/python/qgis-mercicor-plugin/docs/model/index.md'
    text_file = open(output_file, "w+")
    text_file.write(markdown_all)
    text_file.close()


generate_model_doc()
