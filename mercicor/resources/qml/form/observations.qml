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
    <attributeEditorField showLabel="1" index="1" name="nom_station"/>
    <attributeEditorField showLabel="1" index="2" name="station_man"/>
    <attributeEditorField showLabel="1" index="3" name="perc_bsd"/>
    <attributeEditorField showLabel="1" index="4" name="perc_bsm"/>
    <attributeEditorField showLabel="1" index="5" name="datetime_obs"/>
    <attributeEditorField showLabel="1" index="6" name="note_bsd"/>
    <attributeEditorField showLabel="1" index="7" name="note_bsm"/>
    <attributeEditorField showLabel="1" index="8" name="note_ben"/>
    <attributeEditorField showLabel="1" index="9" name="note_man"/>
    <attributeEditorField showLabel="1" index="10" name="note_pmi"/>
    <attributeEditorField showLabel="1" index="11" name="score_station"/>
    <attributeEditorContainer showLabel="1" columnCount="1" groupBox="0" visibilityExpressionEnabled="0" name="Physicochimie" visibilityExpression="">
      <attributeEditorField showLabel="1" index="12" name="phch_temp"/>
      <attributeEditorField showLabel="1" index="13" name="phch_dop"/>
      <attributeEditorField showLabel="1" index="14" name="phch_do"/>
      <attributeEditorField showLabel="1" index="15" name="phch_cond"/>
      <attributeEditorField showLabel="1" index="16" name="phch_sal"/>
      <attributeEditorField showLabel="1" index="17" name="phch_ph"/>
      <attributeEditorField showLabel="1" index="18" name="phch_turb"/>
      <attributeEditorField showLabel="1" index="19" name="phch_sedi"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" groupBox="0" visibilityExpressionEnabled="1" name="Indics Benthos Substrats durs" visibilityExpression="CASE WHEN &quot;station_man&quot; = false THEN true END">
      <attributeEditorField showLabel="1" index="20" name="bsd_recouv_cor"/>
      <attributeEditorField showLabel="1" index="21" name="bsd_p_acrop"/>
      <attributeEditorField showLabel="1" index="22" name="bsd_vital_cor"/>
      <attributeEditorField showLabel="1" index="23" name="bsd_comp_struc"/>
      <attributeEditorField showLabel="1" index="24" name="bsd_taille_cor"/>
      <attributeEditorField showLabel="1" index="25" name="bsd_dens_juv"/>
      <attributeEditorField showLabel="1" index="26" name="bsd_f_sessile"/>
      <attributeEditorField showLabel="1" index="27" name="bsd_recouv_ma"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" groupBox="0" visibilityExpressionEnabled="1" name="Indics Benthos Substrats meubles" visibilityExpression="CASE WHEN &quot;station_man&quot; = false THEN true END">
      <attributeEditorField showLabel="1" index="28" name="bsm_fragm_herb"/>
      <attributeEditorField showLabel="1" index="29" name="bsm_recouv_her"/>
      <attributeEditorField showLabel="1" index="30" name="bsm_haut_herb"/>
      <attributeEditorField showLabel="1" index="31" name="bsm_dens_herb"/>
      <attributeEditorField showLabel="1" index="32" name="bsm_div_herb"/>
      <attributeEditorField showLabel="1" index="33" name="bsm_epibiose"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" groupBox="0" visibilityExpressionEnabled="1" name="Indics Mangroves" visibilityExpression="CASE WHEN &quot;station_man&quot; = true THEN true END">
      <attributeEditorField showLabel="1" index="34" name="man_fragm"/>
      <attributeEditorField showLabel="1" index="35" name="man_recouv"/>
      <attributeEditorField showLabel="1" index="36" name="man_diam_tronc"/>
      <attributeEditorField showLabel="1" index="37" name="man_dens"/>
      <attributeEditorField showLabel="1" index="38" name="man_diversit"/>
      <attributeEditorField showLabel="1" index="39" name="man_vital"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" columnCount="1" groupBox="0" visibilityExpressionEnabled="0" name="Indics Poissons et Macro-invertégrés" visibilityExpression="">
      <attributeEditorField showLabel="1" index="40" name="pmi_div_poi"/>
      <attributeEditorField showLabel="1" index="41" name="pmi_predat_poi"/>
      <attributeEditorField showLabel="1" index="42" name="pmi_scarib_poi"/>
      <attributeEditorField showLabel="1" index="43" name="pmi_macro_inv"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="bsd_comp_struc" editable="1"/>
    <field name="bsd_dens_juv" editable="1"/>
    <field name="bsd_f_sessile" editable="1"/>
    <field name="bsd_p_acrop" editable="1"/>
    <field name="bsd_recouv_cor" editable="1"/>
    <field name="bsd_recouv_ma" editable="1"/>
    <field name="bsd_taille_cor" editable="1"/>
    <field name="bsd_vital_cor" editable="1"/>
    <field name="bsm_dens_herb" editable="1"/>
    <field name="bsm_div_herb" editable="1"/>
    <field name="bsm_epibiose" editable="1"/>
    <field name="bsm_fragm_herb" editable="1"/>
    <field name="bsm_haut_herb" editable="1"/>
    <field name="bsm_recouv_her" editable="1"/>
    <field name="datetime_obs" editable="1"/>
    <field name="id" editable="1"/>
    <field name="man_dens" editable="1"/>
    <field name="man_diam_tronc" editable="1"/>
    <field name="man_diversit" editable="1"/>
    <field name="man_fragm" editable="1"/>
    <field name="man_recouv" editable="1"/>
    <field name="man_vital" editable="1"/>
    <field name="nom_station" editable="1"/>
    <field name="note_ben" editable="1"/>
    <field name="note_bsd" editable="1"/>
    <field name="note_bsm" editable="1"/>
    <field name="note_man" editable="1"/>
    <field name="note_pmi" editable="1"/>
    <field name="perc_bsd" editable="1"/>
    <field name="perc_bsm" editable="1"/>
    <field name="phch_cond" editable="1"/>
    <field name="phch_do" editable="1"/>
    <field name="phch_dop" editable="1"/>
    <field name="phch_ph" editable="1"/>
    <field name="phch_sal" editable="1"/>
    <field name="phch_sedi" editable="1"/>
    <field name="phch_temp" editable="1"/>
    <field name="phch_turb" editable="1"/>
    <field name="pmi_div_poi" editable="1"/>
    <field name="pmi_macro_inv" editable="1"/>
    <field name="pmi_predat_poi" editable="1"/>
    <field name="pmi_scarib_poi" editable="1"/>
    <field name="score_station" editable="1"/>
    <field name="station_man" editable="1"/>
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
    <field name="score_station" labelOnTop="0"/>
    <field name="station_man" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <layerGeometryType>0</layerGeometryType>
</qgis>
