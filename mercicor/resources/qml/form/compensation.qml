<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.10.14-A Coruña" styleCategories="Forms">
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
Les formulaires QGIS peuvent avoir une fonction Python qui sera appelée à l'ouverture du formulaire.

Utilisez cette fonction pour ajouter plus de fonctionnalités à vos formulaires.

Entrez le nom de la fonction dans le champ "Fonction d'initialisation Python".
Voici un exemple à suivre:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
    geom = feature.geometry()
    control = dialog.findChild(QWidget, "MyLineEdit")

]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="coeff_delais" editable="1"/>
    <field name="coeff_risque" editable="1"/>
    <field name="id" editable="1"/>
    <field name="nom" editable="1"/>
    <field name="scenario_id" editable="1"/>
    <field name="type_pression" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="coeff_delais" labelOnTop="0"/>
    <field name="coeff_risque" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="nom" labelOnTop="0"/>
    <field name="scenario_id" labelOnTop="0"/>
    <field name="type_pression" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <layerGeometryType>2</layerGeometryType>
</qgis>
