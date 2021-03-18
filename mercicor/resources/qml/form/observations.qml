<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Forms" version="3.10.14-A Coruña">
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
    control = dialog.findChild(QWidget, "perc_bsd")

]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorField name="nom_station" index="1" showLabel="1"/>
    <attributeEditorField name="station_man" index="2" showLabel="1"/>
    <attributeEditorField name="perc_bsd" index="3" showLabel="1"/>
    <attributeEditorField name="perc_bsm" index="4" showLabel="1"/>
    <attributeEditorField name="datetime_obs" index="5" showLabel="1"/>
    <attributeEditorField name="profondeur" index="6" showLabel="1"/>
    <attributeEditorField name="note_bsd" index="7" showLabel="1"/>
    <attributeEditorField name="note_bsm" index="8" showLabel="1"/>
    <attributeEditorField name="note_ben" index="9" showLabel="1"/>
    <attributeEditorField name="note_man" index="10" showLabel="1"/>
    <attributeEditorField name="note_pmi" index="11" showLabel="1"/>
    <attributeEditorField name="score_mercicor" index="12" showLabel="1"/>
    <attributeEditorContainer groupBox="0" visibilityExpressionEnabled="0" name="Physicochimie" visibilityExpression="" columnCount="1" showLabel="1">
      <attributeEditorField name="phch_temp" index="13" showLabel="1"/>
      <attributeEditorField name="phch_dop" index="14" showLabel="1"/>
      <attributeEditorField name="phch_do" index="15" showLabel="1"/>
      <attributeEditorField name="phch_cond" index="16" showLabel="1"/>
      <attributeEditorField name="phch_sal" index="17" showLabel="1"/>
      <attributeEditorField name="phch_ph" index="18" showLabel="1"/>
      <attributeEditorField name="phch_turb" index="19" showLabel="1"/>
      <attributeEditorField name="phch_sedi" index="20" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer groupBox="0" visibilityExpressionEnabled="1" name="Indics Benthos Substrats durs" visibilityExpression="CASE WHEN &quot;station_man&quot; IS NOT TRUE THEN true END" columnCount="1" showLabel="1">
      <attributeEditorField name="bsd_recouv_cor" index="21" showLabel="1"/>
      <attributeEditorField name="bsd_p_acrop" index="22" showLabel="1"/>
      <attributeEditorField name="bsd_vital_cor" index="23" showLabel="1"/>
      <attributeEditorField name="bsd_comp_struc" index="24" showLabel="1"/>
      <attributeEditorField name="bsd_taille_cor" index="25" showLabel="1"/>
      <attributeEditorField name="bsd_dens_juv" index="26" showLabel="1"/>
      <attributeEditorField name="bsd_f_sessile" index="27" showLabel="1"/>
      <attributeEditorField name="bsd_recouv_ma" index="28" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer groupBox="0" visibilityExpressionEnabled="1" name="Indics Benthos Substrats meubles" visibilityExpression="CASE WHEN &quot;station_man&quot; IS NOT TRUE THEN true END" columnCount="1" showLabel="1">
      <attributeEditorField name="bsm_fragm_herb" index="29" showLabel="1"/>
      <attributeEditorField name="bsm_recouv_her" index="30" showLabel="1"/>
      <attributeEditorField name="bsm_haut_herb" index="31" showLabel="1"/>
      <attributeEditorField name="bsm_dens_herb" index="32" showLabel="1"/>
      <attributeEditorField name="bsm_div_herb" index="33" showLabel="1"/>
      <attributeEditorField name="bsm_epibiose" index="34" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer groupBox="0" visibilityExpressionEnabled="1" name="Indics Mangroves" visibilityExpression="CASE WHEN &quot;station_man&quot; IS true THEN true END" columnCount="1" showLabel="1">
      <attributeEditorField name="man_fragm" index="35" showLabel="1"/>
      <attributeEditorField name="man_recouv" index="36" showLabel="1"/>
      <attributeEditorField name="man_diam_tronc" index="37" showLabel="1"/>
      <attributeEditorField name="man_dens" index="38" showLabel="1"/>
      <attributeEditorField name="man_diversit" index="39" showLabel="1"/>
      <attributeEditorField name="man_vital" index="40" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer groupBox="0" visibilityExpressionEnabled="0" name="Indics Poissons et Macro-invertégrés" visibilityExpression="" columnCount="1" showLabel="1">
      <attributeEditorField name="pmi_div_poi" index="41" showLabel="1"/>
      <attributeEditorField name="pmi_predat_poi" index="42" showLabel="1"/>
      <attributeEditorField name="pmi_scarib_poi" index="43" showLabel="1"/>
      <attributeEditorField name="pmi_macro_inv" index="44" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="bsd_comp_struc"/>
    <field editable="1" name="bsd_dens_juv"/>
    <field editable="1" name="bsd_f_sessile"/>
    <field editable="1" name="bsd_p_acrop"/>
    <field editable="1" name="bsd_recouv_cor"/>
    <field editable="1" name="bsd_recouv_ma"/>
    <field editable="1" name="bsd_taille_cor"/>
    <field editable="1" name="bsd_vital_cor"/>
    <field editable="1" name="bsm_dens_herb"/>
    <field editable="1" name="bsm_div_herb"/>
    <field editable="1" name="bsm_epibiose"/>
    <field editable="1" name="bsm_fragm_herb"/>
    <field editable="1" name="bsm_haut_herb"/>
    <field editable="1" name="bsm_recouv_her"/>
    <field editable="1" name="datetime_obs"/>
    <field editable="1" name="id"/>
    <field editable="1" name="man_dens"/>
    <field editable="1" name="man_diam_tronc"/>
    <field editable="1" name="man_diversit"/>
    <field editable="1" name="man_fragm"/>
    <field editable="1" name="man_recouv"/>
    <field editable="1" name="man_vital"/>
    <field editable="1" name="nom_station"/>
    <field editable="1" name="note_ben"/>
    <field editable="1" name="note_bsd"/>
    <field editable="1" name="note_bsm"/>
    <field editable="1" name="note_man"/>
    <field editable="1" name="note_pmi"/>
    <field editable="1" name="perc_bsd"/>
    <field editable="1" name="perc_bsm"/>
    <field editable="1" name="phch_cond"/>
    <field editable="1" name="phch_do"/>
    <field editable="1" name="phch_dop"/>
    <field editable="1" name="phch_ph"/>
    <field editable="1" name="phch_sal"/>
    <field editable="1" name="phch_sedi"/>
    <field editable="1" name="phch_temp"/>
    <field editable="1" name="phch_turb"/>
    <field editable="1" name="pmi_div_poi"/>
    <field editable="1" name="pmi_macro_inv"/>
    <field editable="1" name="pmi_predat_poi"/>
    <field editable="1" name="pmi_scarib_poi"/>
    <field editable="1" name="profondeur"/>
    <field editable="1" name="score_mercicor"/>
    <field editable="1" name="station_man"/>
  </editable>
  <labelOnTop>
    <field name="bsd_comp_struc" labelOnTop="0"/>
    <field name="bsd_dens_juv" labelOnTop="0"/>
    <field name="bsd_f_sessile" labelOnTop="0"/>
    <field name="bsd_p_acrop" labelOnTop="0"/>
    <field name="bsd_recouv_cor" labelOnTop="0"/>
    <field name="bsd_recouv_ma" labelOnTop="0"/>
    <field name="bsd_taille_cor" labelOnTop="0"/>
    <field name="bsd_vital_cor" labelOnTop="0"/>
    <field name="bsm_dens_herb" labelOnTop="0"/>
    <field name="bsm_div_herb" labelOnTop="0"/>
    <field name="bsm_epibiose" labelOnTop="0"/>
    <field name="bsm_fragm_herb" labelOnTop="0"/>
    <field name="bsm_haut_herb" labelOnTop="0"/>
    <field name="bsm_recouv_her" labelOnTop="0"/>
    <field name="datetime_obs" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="man_dens" labelOnTop="0"/>
    <field name="man_diam_tronc" labelOnTop="0"/>
    <field name="man_diversit" labelOnTop="0"/>
    <field name="man_fragm" labelOnTop="0"/>
    <field name="man_recouv" labelOnTop="0"/>
    <field name="man_vital" labelOnTop="0"/>
    <field name="nom_station" labelOnTop="0"/>
    <field name="note_ben" labelOnTop="0"/>
    <field name="note_bsd" labelOnTop="0"/>
    <field name="note_bsm" labelOnTop="0"/>
    <field name="note_man" labelOnTop="0"/>
    <field name="note_pmi" labelOnTop="0"/>
    <field name="perc_bsd" labelOnTop="0"/>
    <field name="perc_bsm" labelOnTop="0"/>
    <field name="phch_cond" labelOnTop="0"/>
    <field name="phch_do" labelOnTop="0"/>
    <field name="phch_dop" labelOnTop="0"/>
    <field name="phch_ph" labelOnTop="0"/>
    <field name="phch_sal" labelOnTop="0"/>
    <field name="phch_sedi" labelOnTop="0"/>
    <field name="phch_temp" labelOnTop="0"/>
    <field name="phch_turb" labelOnTop="0"/>
    <field name="pmi_div_poi" labelOnTop="0"/>
    <field name="pmi_macro_inv" labelOnTop="0"/>
    <field name="pmi_predat_poi" labelOnTop="0"/>
    <field name="pmi_scarib_poi" labelOnTop="0"/>
    <field name="profondeur" labelOnTop="0"/>
    <field name="score_mercicor" labelOnTop="0"/>
    <field name="station_man" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <layerGeometryType>0</layerGeometryType>
</qgis>
