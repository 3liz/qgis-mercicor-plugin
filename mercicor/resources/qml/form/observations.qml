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
    <attributeEditorField index="1" showLabel="1" name="nom_station"/>
    <attributeEditorField index="2" showLabel="1" name="station_man"/>
    <attributeEditorField index="3" showLabel="1" name="perc_bsd"/>
    <attributeEditorField index="4" showLabel="1" name="perc_bsm"/>
    <attributeEditorField index="5" showLabel="1" name="datetime_obs"/>
    <attributeEditorField index="6" showLabel="1" name="note_bsd"/>
    <attributeEditorField index="7" showLabel="1" name="note_bsm"/>
    <attributeEditorField index="8" showLabel="1" name="note_ben"/>
    <attributeEditorField index="9" showLabel="1" name="note_man"/>
    <attributeEditorField index="10" showLabel="1" name="note_pmi"/>
    <attributeEditorField index="11" showLabel="1" name="score_station"/>
    <attributeEditorContainer columnCount="1" groupBox="0" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" name="Physicochimie">
      <attributeEditorField index="12" showLabel="1" name="phch_temp"/>
      <attributeEditorField index="13" showLabel="1" name="phch_dop"/>
      <attributeEditorField index="14" showLabel="1" name="phch_do"/>
      <attributeEditorField index="15" showLabel="1" name="phch_cond"/>
      <attributeEditorField index="16" showLabel="1" name="phch_sal"/>
      <attributeEditorField index="17" showLabel="1" name="phch_ph"/>
      <attributeEditorField index="18" showLabel="1" name="phch_turb"/>
      <attributeEditorField index="19" showLabel="1" name="phch_sedi"/>
    </attributeEditorContainer>
    <attributeEditorContainer columnCount="1" groupBox="0" visibilityExpression="CASE WHEN &quot;station_man&quot; IS NOT TRUE THEN true END" showLabel="1" visibilityExpressionEnabled="1" name="Indics Benthos Substrats durs">
      <attributeEditorField index="20" showLabel="1" name="bsd_recouv_cor"/>
      <attributeEditorField index="21" showLabel="1" name="bsd_p_acrop"/>
      <attributeEditorField index="22" showLabel="1" name="bsd_vital_cor"/>
      <attributeEditorField index="23" showLabel="1" name="bsd_comp_struc"/>
      <attributeEditorField index="24" showLabel="1" name="bsd_taille_cor"/>
      <attributeEditorField index="25" showLabel="1" name="bsd_dens_juv"/>
      <attributeEditorField index="26" showLabel="1" name="bsd_f_sessile"/>
      <attributeEditorField index="27" showLabel="1" name="bsd_recouv_ma"/>
    </attributeEditorContainer>
    <attributeEditorContainer columnCount="1" groupBox="0" visibilityExpression="CASE WHEN &quot;station_man&quot; IS NOT TRUE THEN true END" showLabel="1" visibilityExpressionEnabled="1" name="Indics Benthos Substrats meubles">
      <attributeEditorField index="28" showLabel="1" name="bsm_fragm_herb"/>
      <attributeEditorField index="29" showLabel="1" name="bsm_recouv_her"/>
      <attributeEditorField index="30" showLabel="1" name="bsm_haut_herb"/>
      <attributeEditorField index="31" showLabel="1" name="bsm_dens_herb"/>
      <attributeEditorField index="32" showLabel="1" name="bsm_div_herb"/>
      <attributeEditorField index="33" showLabel="1" name="bsm_epibiose"/>
    </attributeEditorContainer>
    <attributeEditorContainer columnCount="1" groupBox="0" visibilityExpression="CASE WHEN &quot;station_man&quot; IS true THEN true END" showLabel="1" visibilityExpressionEnabled="1" name="Indics Mangroves">
      <attributeEditorField index="34" showLabel="1" name="man_fragm"/>
      <attributeEditorField index="35" showLabel="1" name="man_recouv"/>
      <attributeEditorField index="36" showLabel="1" name="man_diam_tronc"/>
      <attributeEditorField index="37" showLabel="1" name="man_dens"/>
      <attributeEditorField index="38" showLabel="1" name="man_diversit"/>
      <attributeEditorField index="39" showLabel="1" name="man_vital"/>
    </attributeEditorContainer>
    <attributeEditorContainer columnCount="1" groupBox="0" visibilityExpression="" showLabel="1" visibilityExpressionEnabled="0" name="Indics Poissons et Macro-invertégrés">
      <attributeEditorField index="40" showLabel="1" name="pmi_div_poi"/>
      <attributeEditorField index="41" showLabel="1" name="pmi_predat_poi"/>
      <attributeEditorField index="42" showLabel="1" name="pmi_scarib_poi"/>
      <attributeEditorField index="43" showLabel="1" name="pmi_macro_inv"/>
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
    <field editable="1" name="score_station"/>
    <field editable="1" name="station_man"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="bsd_comp_struc"/>
    <field labelOnTop="0" name="bsd_dens_juv"/>
    <field labelOnTop="0" name="bsd_f_sessile"/>
    <field labelOnTop="0" name="bsd_p_acrop"/>
    <field labelOnTop="0" name="bsd_recouv_cor"/>
    <field labelOnTop="0" name="bsd_recouv_ma"/>
    <field labelOnTop="0" name="bsd_taille_cor"/>
    <field labelOnTop="0" name="bsd_vital_cor"/>
    <field labelOnTop="0" name="bsm_dens_herb"/>
    <field labelOnTop="0" name="bsm_div_herb"/>
    <field labelOnTop="0" name="bsm_epibiose"/>
    <field labelOnTop="0" name="bsm_fragm_herb"/>
    <field labelOnTop="0" name="bsm_haut_herb"/>
    <field labelOnTop="0" name="bsm_recouv_her"/>
    <field labelOnTop="0" name="datetime_obs"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="man_dens"/>
    <field labelOnTop="0" name="man_diam_tronc"/>
    <field labelOnTop="0" name="man_diversit"/>
    <field labelOnTop="0" name="man_fragm"/>
    <field labelOnTop="0" name="man_recouv"/>
    <field labelOnTop="0" name="man_vital"/>
    <field labelOnTop="0" name="nom_station"/>
    <field labelOnTop="0" name="note_ben"/>
    <field labelOnTop="0" name="note_bsd"/>
    <field labelOnTop="0" name="note_bsm"/>
    <field labelOnTop="0" name="note_man"/>
    <field labelOnTop="0" name="note_pmi"/>
    <field labelOnTop="0" name="perc_bsd"/>
    <field labelOnTop="0" name="perc_bsm"/>
    <field labelOnTop="0" name="phch_cond"/>
    <field labelOnTop="0" name="phch_do"/>
    <field labelOnTop="0" name="phch_dop"/>
    <field labelOnTop="0" name="phch_ph"/>
    <field labelOnTop="0" name="phch_sal"/>
    <field labelOnTop="0" name="phch_sedi"/>
    <field labelOnTop="0" name="phch_temp"/>
    <field labelOnTop="0" name="phch_turb"/>
    <field labelOnTop="0" name="pmi_div_poi"/>
    <field labelOnTop="0" name="pmi_macro_inv"/>
    <field labelOnTop="0" name="pmi_predat_poi"/>
    <field labelOnTop="0" name="pmi_scarib_poi"/>
    <field labelOnTop="0" name="score_station"/>
    <field labelOnTop="0" name="station_man"/>
  </labelOnTop>
  <widgets/>
  <layerGeometryType>0</layerGeometryType>
</qgis>
