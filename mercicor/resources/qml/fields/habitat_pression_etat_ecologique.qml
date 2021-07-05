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
    control = dialog.findChild(QWidget, "perc_bsd")

]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorField index="37" showLabel="1" name="hab_nom"/>
    <attributeEditorField index="38" showLabel="1" name="hab_facies"/>
    <attributeEditorField index="72" showLabel="1" name="pression_type_pression"/>
    <attributeEditorField index="74" showLabel="1" name="scenario_nom"/>
    <attributeEditorField index="4" showLabel="1" name="station_man"/>
    <attributeEditorContainer visibilityExpression="" groupBox="0" showLabel="1" visibilityExpressionEnabled="0" name="Notes &amp; Scores" columnCount="2">
      <attributeEditorContainer visibilityExpression="" groupBox="1" showLabel="1" visibilityExpressionEnabled="0" name="Pression" columnCount="1">
        <attributeEditorField index="5" showLabel="1" name="perc_bsd"/>
        <attributeEditorField index="6" showLabel="1" name="perc_bsm"/>
        <attributeEditorField index="31" showLabel="1" name="note_bsd"/>
        <attributeEditorField index="32" showLabel="1" name="note_bsm"/>
        <attributeEditorField index="33" showLabel="1" name="note_ben"/>
        <attributeEditorField index="34" showLabel="1" name="note_man"/>
        <attributeEditorField index="35" showLabel="1" name="note_pmi"/>
        <attributeEditorField index="36" showLabel="1" name="score_mercicor"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" groupBox="1" showLabel="1" visibilityExpressionEnabled="0" name="Habitat" columnCount="1">
        <attributeEditorField index="40" showLabel="1" name="hab_perc_bsd"/>
        <attributeEditorField index="41" showLabel="1" name="hab_perc_bsm"/>
        <attributeEditorField index="66" showLabel="1" name="hab_note_bsd"/>
        <attributeEditorField index="67" showLabel="1" name="hab_note_bsm"/>
        <attributeEditorField index="68" showLabel="1" name="hab_note_ben"/>
        <attributeEditorField index="69" showLabel="1" name="hab_note_man"/>
        <attributeEditorField index="70" showLabel="1" name="hab_note_pmi"/>
        <attributeEditorField index="71" showLabel="1" name="hab_score_mercicor"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="CASE WHEN &quot;station_man&quot; IS NOT true THEN true END" groupBox="0" showLabel="1" visibilityExpressionEnabled="1" name="Indics Benthos Substrats durs" columnCount="2">
      <attributeEditorContainer visibilityExpression="" groupBox="1" showLabel="1" visibilityExpressionEnabled="0" name="Pression" columnCount="1">
        <attributeEditorField index="7" showLabel="1" name="bsd_recouv_cor"/>
        <attributeEditorField index="8" showLabel="1" name="bsd_p_acrop"/>
        <attributeEditorField index="9" showLabel="1" name="bsd_vital_cor"/>
        <attributeEditorField index="10" showLabel="1" name="bsd_comp_struc"/>
        <attributeEditorField index="11" showLabel="1" name="bsd_taille_cor"/>
        <attributeEditorField index="12" showLabel="1" name="bsd_dens_juv"/>
        <attributeEditorField index="13" showLabel="1" name="bsd_f_sessile"/>
        <attributeEditorField index="14" showLabel="1" name="bsd_recouv_ma"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" groupBox="1" showLabel="1" visibilityExpressionEnabled="0" name="Habitat" columnCount="1">
        <attributeEditorField index="42" showLabel="1" name="hab_bsd_recouv_cor"/>
        <attributeEditorField index="43" showLabel="1" name="hab_bsd_p_acrop"/>
        <attributeEditorField index="44" showLabel="1" name="hab_bsd_vital_cor"/>
        <attributeEditorField index="45" showLabel="1" name="hab_bsd_comp_struc"/>
        <attributeEditorField index="46" showLabel="1" name="hab_bsd_taille_cor"/>
        <attributeEditorField index="47" showLabel="1" name="hab_bsd_dens_juv"/>
        <attributeEditorField index="48" showLabel="1" name="hab_bsd_f_sessile"/>
        <attributeEditorField index="49" showLabel="1" name="hab_bsd_recouv_ma"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="CASE WHEN &quot;station_man&quot; IS NOT true THEN true END" groupBox="0" showLabel="1" visibilityExpressionEnabled="1" name="Indics Benthos Substrats meubles" columnCount="2">
      <attributeEditorContainer visibilityExpression="" groupBox="1" showLabel="1" visibilityExpressionEnabled="0" name="Pression" columnCount="1">
        <attributeEditorField index="15" showLabel="1" name="bsm_fragm_herb"/>
        <attributeEditorField index="16" showLabel="1" name="bsm_recouv_her"/>
        <attributeEditorField index="17" showLabel="1" name="bsm_haut_herb"/>
        <attributeEditorField index="18" showLabel="1" name="bsm_dens_herb"/>
        <attributeEditorField index="19" showLabel="1" name="bsm_div_herb"/>
        <attributeEditorField index="20" showLabel="1" name="bsm_epibiose"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" groupBox="1" showLabel="1" visibilityExpressionEnabled="0" name="Habitat" columnCount="1">
        <attributeEditorField index="50" showLabel="1" name="hab_bsm_fragm_herb"/>
        <attributeEditorField index="51" showLabel="1" name="hab_bsm_recouv_her"/>
        <attributeEditorField index="52" showLabel="1" name="hab_bsm_haut_herb"/>
        <attributeEditorField index="53" showLabel="1" name="hab_bsm_dens_herb"/>
        <attributeEditorField index="54" showLabel="1" name="hab_bsm_div_herb"/>
        <attributeEditorField index="55" showLabel="1" name="hab_bsm_epibiose"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="CASE WHEN &quot;station_man&quot; IS  true THEN true END" groupBox="0" showLabel="1" visibilityExpressionEnabled="1" name="Indics Mangroves" columnCount="2">
      <attributeEditorContainer visibilityExpression="" groupBox="1" showLabel="1" visibilityExpressionEnabled="0" name="Pression" columnCount="1">
        <attributeEditorField index="21" showLabel="1" name="man_fragm"/>
        <attributeEditorField index="22" showLabel="1" name="man_recouv"/>
        <attributeEditorField index="23" showLabel="1" name="man_diam_tronc"/>
        <attributeEditorField index="24" showLabel="1" name="man_dens"/>
        <attributeEditorField index="25" showLabel="1" name="man_diversit"/>
        <attributeEditorField index="26" showLabel="1" name="man_vital"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" groupBox="1" showLabel="1" visibilityExpressionEnabled="0" name="Habitat" columnCount="1">
        <attributeEditorField index="56" showLabel="1" name="hab_man_fragm"/>
        <attributeEditorField index="57" showLabel="1" name="hab_man_recouv"/>
        <attributeEditorField index="58" showLabel="1" name="hab_man_diam_tronc"/>
        <attributeEditorField index="59" showLabel="1" name="hab_man_dens"/>
        <attributeEditorField index="60" showLabel="1" name="hab_man_diversit"/>
        <attributeEditorField index="61" showLabel="1" name="hab_man_vital"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpression="" groupBox="0" showLabel="1" visibilityExpressionEnabled="0" name="Indics Poissons et Macro-invertégrés" columnCount="2">
      <attributeEditorContainer visibilityExpression="" groupBox="1" showLabel="1" visibilityExpressionEnabled="0" name="Pression" columnCount="1">
        <attributeEditorField index="27" showLabel="1" name="pmi_div_poi"/>
        <attributeEditorField index="28" showLabel="1" name="pmi_predat_poi"/>
        <attributeEditorField index="29" showLabel="1" name="pmi_scarib_poi"/>
        <attributeEditorField index="30" showLabel="1" name="pmi_macro_inv"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpression="" groupBox="1" showLabel="1" visibilityExpressionEnabled="0" name="habitat" columnCount="1">
        <attributeEditorField index="62" showLabel="1" name="hab_pmi_div_poi"/>
        <attributeEditorField index="63" showLabel="1" name="hab_pmi_predat_poi"/>
        <attributeEditorField index="64" showLabel="1" name="hab_pmi_scarib_poi"/>
        <attributeEditorField index="65" showLabel="1" name="hab_pmi_macro_inv"/>
      </attributeEditorContainer>
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
    <field name="hab_bsd_comp_struc" editable="0"/>
    <field name="hab_bsd_dens_juv" editable="0"/>
    <field name="hab_bsd_f_sessile" editable="0"/>
    <field name="hab_bsd_p_acrop" editable="0"/>
    <field name="hab_bsd_recouv_cor" editable="0"/>
    <field name="hab_bsd_recouv_ma" editable="0"/>
    <field name="hab_bsd_taille_cor" editable="0"/>
    <field name="hab_bsd_vital_cor" editable="0"/>
    <field name="hab_bsm_dens_herb" editable="0"/>
    <field name="hab_bsm_div_herb" editable="0"/>
    <field name="hab_bsm_epibiose" editable="0"/>
    <field name="hab_bsm_fragm_herb" editable="0"/>
    <field name="hab_bsm_haut_herb" editable="0"/>
    <field name="hab_bsm_recouv_her" editable="0"/>
    <field name="hab_facies" editable="0"/>
    <field name="hab_man_dens" editable="0"/>
    <field name="hab_man_diam_tronc" editable="0"/>
    <field name="hab_man_diversit" editable="0"/>
    <field name="hab_man_fragm" editable="0"/>
    <field name="hab_man_recouv" editable="0"/>
    <field name="hab_man_vital" editable="0"/>
    <field name="hab_nom" editable="0"/>
    <field name="hab_note_ben" editable="0"/>
    <field name="hab_note_bsd" editable="0"/>
    <field name="hab_note_bsm" editable="0"/>
    <field name="hab_note_man" editable="0"/>
    <field name="hab_note_pmi" editable="0"/>
    <field name="hab_perc_bsd" editable="0"/>
    <field name="hab_perc_bsm" editable="0"/>
    <field name="hab_pmi_div_poi" editable="0"/>
    <field name="hab_pmi_macro_inv" editable="0"/>
    <field name="hab_pmi_predat_poi" editable="0"/>
    <field name="hab_pmi_scarib_poi" editable="0"/>
    <field name="hab_score_mercicor" editable="0"/>
    <field name="hab_station_man" editable="0"/>
    <field name="habitat_id" editable="1"/>
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
    <field name="perte_ben" editable="0"/>
    <field name="perte_bsd" editable="0"/>
    <field name="perte_bsm" editable="0"/>
    <field name="perte_man" editable="0"/>
    <field name="perte_mercicor" editable="0"/>
    <field name="perte_pmi" editable="0"/>
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
    <field name="pression_id" editable="1"/>
    <field name="pression_scenario_id" editable="0"/>
    <field name="pression_type_pression" editable="0"/>
    <field name="profondeur" editable="1"/>
    <field name="scenario_id" editable="1"/>
    <field name="scenario_nom" editable="0"/>
    <field name="scenario_perte_ben" editable="0"/>
    <field name="scenario_perte_bsd" editable="0"/>
    <field name="scenario_perte_bsm" editable="0"/>
    <field name="scenario_perte_man" editable="0"/>
    <field name="scenario_perte_mercicor" editable="0"/>
    <field name="scenario_perte_pmi" editable="0"/>
    <field name="score_mercicor" editable="1"/>
    <field name="station_man" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="1" name="bsd_comp_struc"/>
    <field labelOnTop="1" name="bsd_dens_juv"/>
    <field labelOnTop="1" name="bsd_f_sessile"/>
    <field labelOnTop="1" name="bsd_p_acrop"/>
    <field labelOnTop="1" name="bsd_recouv_cor"/>
    <field labelOnTop="1" name="bsd_recouv_ma"/>
    <field labelOnTop="1" name="bsd_taille_cor"/>
    <field labelOnTop="1" name="bsd_vital_cor"/>
    <field labelOnTop="1" name="bsm_dens_herb"/>
    <field labelOnTop="1" name="bsm_div_herb"/>
    <field labelOnTop="1" name="bsm_epibiose"/>
    <field labelOnTop="1" name="bsm_fragm_herb"/>
    <field labelOnTop="1" name="bsm_haut_herb"/>
    <field labelOnTop="1" name="bsm_recouv_her"/>
    <field labelOnTop="0" name="datetime_obs"/>
    <field labelOnTop="1" name="hab_bsd_comp_struc"/>
    <field labelOnTop="1" name="hab_bsd_dens_juv"/>
    <field labelOnTop="1" name="hab_bsd_f_sessile"/>
    <field labelOnTop="1" name="hab_bsd_p_acrop"/>
    <field labelOnTop="1" name="hab_bsd_recouv_cor"/>
    <field labelOnTop="1" name="hab_bsd_recouv_ma"/>
    <field labelOnTop="1" name="hab_bsd_taille_cor"/>
    <field labelOnTop="1" name="hab_bsd_vital_cor"/>
    <field labelOnTop="1" name="hab_bsm_dens_herb"/>
    <field labelOnTop="1" name="hab_bsm_div_herb"/>
    <field labelOnTop="1" name="hab_bsm_epibiose"/>
    <field labelOnTop="1" name="hab_bsm_fragm_herb"/>
    <field labelOnTop="1" name="hab_bsm_haut_herb"/>
    <field labelOnTop="1" name="hab_bsm_recouv_her"/>
    <field labelOnTop="0" name="hab_facies"/>
    <field labelOnTop="1" name="hab_man_dens"/>
    <field labelOnTop="1" name="hab_man_diam_tronc"/>
    <field labelOnTop="1" name="hab_man_diversit"/>
    <field labelOnTop="1" name="hab_man_fragm"/>
    <field labelOnTop="1" name="hab_man_recouv"/>
    <field labelOnTop="1" name="hab_man_vital"/>
    <field labelOnTop="0" name="hab_nom"/>
    <field labelOnTop="1" name="hab_note_ben"/>
    <field labelOnTop="1" name="hab_note_bsd"/>
    <field labelOnTop="1" name="hab_note_bsm"/>
    <field labelOnTop="1" name="hab_note_man"/>
    <field labelOnTop="1" name="hab_note_pmi"/>
    <field labelOnTop="1" name="hab_perc_bsd"/>
    <field labelOnTop="1" name="hab_perc_bsm"/>
    <field labelOnTop="1" name="hab_pmi_div_poi"/>
    <field labelOnTop="1" name="hab_pmi_macro_inv"/>
    <field labelOnTop="1" name="hab_pmi_predat_poi"/>
    <field labelOnTop="1" name="hab_pmi_scarib_poi"/>
    <field labelOnTop="1" name="hab_score_mercicor"/>
    <field labelOnTop="0" name="hab_station_man"/>
    <field labelOnTop="0" name="habitat_id"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="1" name="man_dens"/>
    <field labelOnTop="1" name="man_diam_tronc"/>
    <field labelOnTop="1" name="man_diversit"/>
    <field labelOnTop="1" name="man_fragm"/>
    <field labelOnTop="1" name="man_recouv"/>
    <field labelOnTop="1" name="man_vital"/>
    <field labelOnTop="0" name="nom_station"/>
    <field labelOnTop="1" name="note_ben"/>
    <field labelOnTop="1" name="note_bsd"/>
    <field labelOnTop="1" name="note_bsm"/>
    <field labelOnTop="1" name="note_man"/>
    <field labelOnTop="1" name="note_pmi"/>
    <field labelOnTop="1" name="perc_bsd"/>
    <field labelOnTop="1" name="perc_bsm"/>
    <field labelOnTop="0" name="perte_ben"/>
    <field labelOnTop="0" name="perte_bsd"/>
    <field labelOnTop="0" name="perte_bsm"/>
    <field labelOnTop="0" name="perte_man"/>
    <field labelOnTop="0" name="perte_mercicor"/>
    <field labelOnTop="0" name="perte_pmi"/>
    <field labelOnTop="0" name="phch_cond"/>
    <field labelOnTop="0" name="phch_do"/>
    <field labelOnTop="0" name="phch_dop"/>
    <field labelOnTop="0" name="phch_ph"/>
    <field labelOnTop="0" name="phch_sal"/>
    <field labelOnTop="0" name="phch_sedi"/>
    <field labelOnTop="0" name="phch_temp"/>
    <field labelOnTop="0" name="phch_turb"/>
    <field labelOnTop="1" name="pmi_div_poi"/>
    <field labelOnTop="1" name="pmi_macro_inv"/>
    <field labelOnTop="1" name="pmi_predat_poi"/>
    <field labelOnTop="1" name="pmi_scarib_poi"/>
    <field labelOnTop="0" name="pression_id"/>
    <field labelOnTop="0" name="pression_scenario_id"/>
    <field labelOnTop="0" name="pression_type_pression"/>
    <field labelOnTop="0" name="profondeur"/>
    <field labelOnTop="0" name="scenario_id"/>
    <field labelOnTop="0" name="scenario_nom"/>
    <field labelOnTop="0" name="scenario_perte_ben"/>
    <field labelOnTop="0" name="scenario_perte_bsd"/>
    <field labelOnTop="0" name="scenario_perte_bsm"/>
    <field labelOnTop="0" name="scenario_perte_man"/>
    <field labelOnTop="0" name="scenario_perte_mercicor"/>
    <field labelOnTop="0" name="scenario_perte_pmi"/>
    <field labelOnTop="1" name="score_mercicor"/>
    <field labelOnTop="0" name="station_man"/>
  </labelOnTop>
  <widgets>
    <widget name="habitat_pression_etat_ecologique-habitat">
      <config type="Map">
        <Option type="QString" value="" name="nm-rel"/>
      </config>
    </widget>
    <widget name="pression_habitat_pression_etat_ecologique-pression">
      <config type="Map">
        <Option type="QString" value="" name="nm-rel"/>
      </config>
    </widget>
  </widgets>
  <layerGeometryType>2</layerGeometryType>
</qgis>
