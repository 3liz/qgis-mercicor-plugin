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
    <attributeEditorField name="hab_nom" showLabel="1" index="37"/>
    <attributeEditorField name="hab_facies" showLabel="1" index="38"/>
    <attributeEditorField name="pression_type_pression" showLabel="1" index="72"/>
    <attributeEditorField name="scenario_nom" showLabel="1" index="74"/>
    <attributeEditorField name="station_man" showLabel="1" index="4"/>
    <attributeEditorContainer visibilityExpressionEnabled="0" name="Notes &amp; Scores" showLabel="1" groupBox="0" visibilityExpression="" columnCount="2">
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Pression" showLabel="1" groupBox="1" visibilityExpression="" columnCount="1">
        <attributeEditorField name="perc_bsd" showLabel="1" index="5"/>
        <attributeEditorField name="perc_bsm" showLabel="1" index="6"/>
        <attributeEditorField name="note_bsd" showLabel="1" index="31"/>
        <attributeEditorField name="note_bsm" showLabel="1" index="32"/>
        <attributeEditorField name="note_ben" showLabel="1" index="33"/>
        <attributeEditorField name="note_man" showLabel="1" index="34"/>
        <attributeEditorField name="note_pmi" showLabel="1" index="35"/>
        <attributeEditorField name="score_mercicor" showLabel="1" index="36"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Habitat" showLabel="1" groupBox="1" visibilityExpression="" columnCount="1">
        <attributeEditorField name="hab_perc_bsd" showLabel="1" index="40"/>
        <attributeEditorField name="hab_perc_bsm" showLabel="1" index="41"/>
        <attributeEditorField name="hab_note_bsd" showLabel="1" index="66"/>
        <attributeEditorField name="hab_note_bsm" showLabel="1" index="67"/>
        <attributeEditorField name="hab_note_ben" showLabel="1" index="68"/>
        <attributeEditorField name="hab_note_man" showLabel="1" index="69"/>
        <attributeEditorField name="hab_note_pmi" showLabel="1" index="70"/>
        <attributeEditorField name="hab_score_mercicor" showLabel="1" index="71"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpressionEnabled="1" name="Indics Benthos Substrats durs" showLabel="1" groupBox="0" visibilityExpression="CASE WHEN &quot;station_man&quot; IS NOT true THEN true END" columnCount="2">
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Pression" showLabel="1" groupBox="1" visibilityExpression="" columnCount="1">
        <attributeEditorField name="bsd_recouv_cor" showLabel="1" index="7"/>
        <attributeEditorField name="bsd_p_acrop" showLabel="1" index="8"/>
        <attributeEditorField name="bsd_vital_cor" showLabel="1" index="9"/>
        <attributeEditorField name="bsd_comp_struc" showLabel="1" index="10"/>
        <attributeEditorField name="bsd_taille_cor" showLabel="1" index="11"/>
        <attributeEditorField name="bsd_dens_juv" showLabel="1" index="12"/>
        <attributeEditorField name="bsd_f_sessile" showLabel="1" index="13"/>
        <attributeEditorField name="bsd_recouv_ma" showLabel="1" index="14"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Habitat" showLabel="1" groupBox="1" visibilityExpression="" columnCount="1">
        <attributeEditorField name="hab_bsd_recouv_ma" showLabel="1" index="49"/>
        <attributeEditorField name="hab_bsd_f_sessile" showLabel="1" index="48"/>
        <attributeEditorField name="hab_bsd_dens_juv" showLabel="1" index="47"/>
        <attributeEditorField name="hab_bsd_taille_cor" showLabel="1" index="46"/>
        <attributeEditorField name="hab_bsd_comp_struc" showLabel="1" index="45"/>
        <attributeEditorField name="hab_bsd_vital_cor" showLabel="1" index="44"/>
        <attributeEditorField name="hab_bsd_p_acrop" showLabel="1" index="43"/>
        <attributeEditorField name="hab_bsd_recouv_cor" showLabel="1" index="42"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpressionEnabled="1" name="Indics Benthos Substrats meubles" showLabel="1" groupBox="0" visibilityExpression="CASE WHEN &quot;station_man&quot; IS NOT true THEN true END" columnCount="2">
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Pression" showLabel="1" groupBox="1" visibilityExpression="" columnCount="1">
        <attributeEditorField name="bsm_fragm_herb" showLabel="1" index="15"/>
        <attributeEditorField name="bsm_recouv_her" showLabel="1" index="16"/>
        <attributeEditorField name="bsm_haut_herb" showLabel="1" index="17"/>
        <attributeEditorField name="bsm_dens_herb" showLabel="1" index="18"/>
        <attributeEditorField name="bsm_div_herb" showLabel="1" index="19"/>
        <attributeEditorField name="bsm_epibiose" showLabel="1" index="20"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Habitat" showLabel="1" groupBox="1" visibilityExpression="" columnCount="1">
        <attributeEditorField name="hab_bsm_fragm_herb" showLabel="1" index="50"/>
        <attributeEditorField name="hab_bsm_recouv_her" showLabel="1" index="51"/>
        <attributeEditorField name="hab_bsm_haut_herb" showLabel="1" index="52"/>
        <attributeEditorField name="hab_bsm_dens_herb" showLabel="1" index="53"/>
        <attributeEditorField name="hab_bsm_div_herb" showLabel="1" index="54"/>
        <attributeEditorField name="hab_bsm_epibiose" showLabel="1" index="55"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpressionEnabled="1" name="Indics Mangroves" showLabel="1" groupBox="0" visibilityExpression="CASE WHEN &quot;station_man&quot; IS  true THEN true END" columnCount="2">
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Pression" showLabel="1" groupBox="1" visibilityExpression="" columnCount="1">
        <attributeEditorField name="man_fragm" showLabel="1" index="21"/>
        <attributeEditorField name="man_recouv" showLabel="1" index="22"/>
        <attributeEditorField name="man_diam_tronc" showLabel="1" index="23"/>
        <attributeEditorField name="man_dens" showLabel="1" index="24"/>
        <attributeEditorField name="man_diversit" showLabel="1" index="25"/>
        <attributeEditorField name="man_vital" showLabel="1" index="26"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Habitat" showLabel="1" groupBox="1" visibilityExpression="" columnCount="1">
        <attributeEditorField name="hab_man_fragm" showLabel="1" index="56"/>
        <attributeEditorField name="hab_man_recouv" showLabel="1" index="57"/>
        <attributeEditorField name="hab_man_diam_tronc" showLabel="1" index="58"/>
        <attributeEditorField name="hab_man_dens" showLabel="1" index="59"/>
        <attributeEditorField name="hab_man_diversit" showLabel="1" index="60"/>
        <attributeEditorField name="hab_man_vital" showLabel="1" index="61"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
    <attributeEditorContainer visibilityExpressionEnabled="0" name="Indics Poissons et Macro-invertégrés" showLabel="1" groupBox="0" visibilityExpression="" columnCount="2">
      <attributeEditorContainer visibilityExpressionEnabled="0" name="Pression" showLabel="1" groupBox="1" visibilityExpression="" columnCount="1">
        <attributeEditorField name="pmi_div_poi" showLabel="1" index="27"/>
        <attributeEditorField name="pmi_predat_poi" showLabel="1" index="28"/>
        <attributeEditorField name="pmi_scarib_poi" showLabel="1" index="29"/>
        <attributeEditorField name="pmi_macro_inv" showLabel="1" index="30"/>
      </attributeEditorContainer>
      <attributeEditorContainer visibilityExpressionEnabled="0" name="habitat" showLabel="1" groupBox="1" visibilityExpression="" columnCount="1">
        <attributeEditorField name="hab_pmi_div_poi" showLabel="1" index="62"/>
        <attributeEditorField name="hab_pmi_predat_poi" showLabel="1" index="63"/>
        <attributeEditorField name="hab_pmi_scarib_poi" showLabel="1" index="64"/>
        <attributeEditorField name="hab_pmi_macro_inv" showLabel="1" index="65"/>
      </attributeEditorContainer>
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
    <field editable="0" name="hab_bsd_comp_struc"/>
    <field editable="0" name="hab_bsd_dens_juv"/>
    <field editable="0" name="hab_bsd_f_sessile"/>
    <field editable="0" name="hab_bsd_p_acrop"/>
    <field editable="0" name="hab_bsd_recouv_cor"/>
    <field editable="0" name="hab_bsd_recouv_ma"/>
    <field editable="0" name="hab_bsd_taille_cor"/>
    <field editable="0" name="hab_bsd_vital_cor"/>
    <field editable="0" name="hab_bsm_dens_herb"/>
    <field editable="0" name="hab_bsm_div_herb"/>
    <field editable="0" name="hab_bsm_epibiose"/>
    <field editable="0" name="hab_bsm_fragm_herb"/>
    <field editable="0" name="hab_bsm_haut_herb"/>
    <field editable="0" name="hab_bsm_recouv_her"/>
    <field editable="0" name="hab_facies"/>
    <field editable="0" name="hab_man_dens"/>
    <field editable="0" name="hab_man_diam_tronc"/>
    <field editable="0" name="hab_man_diversit"/>
    <field editable="0" name="hab_man_fragm"/>
    <field editable="0" name="hab_man_recouv"/>
    <field editable="0" name="hab_man_vital"/>
    <field editable="0" name="hab_nom"/>
    <field editable="0" name="hab_note_ben"/>
    <field editable="0" name="hab_note_bsd"/>
    <field editable="0" name="hab_note_bsm"/>
    <field editable="0" name="hab_note_man"/>
    <field editable="0" name="hab_note_pmi"/>
    <field editable="0" name="hab_perc_bsd"/>
    <field editable="0" name="hab_perc_bsm"/>
    <field editable="0" name="hab_pmi_div_poi"/>
    <field editable="0" name="hab_pmi_macro_inv"/>
    <field editable="0" name="hab_pmi_predat_poi"/>
    <field editable="0" name="hab_pmi_scarib_poi"/>
    <field editable="0" name="hab_score_mercicor"/>
    <field editable="0" name="hab_station_man"/>
    <field editable="1" name="habitat_id"/>
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
    <field editable="1" name="pression_id"/>
    <field editable="0" name="pression_scenario_id"/>
    <field editable="0" name="pression_type_pression"/>
    <field editable="1" name="profondeur"/>
    <field editable="1" name="scenario_id"/>
    <field editable="0" name="scenario_nom"/>
    <field editable="0" name="scenario_perte_ben"/>
    <field editable="0" name="scenario_perte_bsd"/>
    <field editable="0" name="scenario_perte_bsm"/>
    <field editable="0" name="scenario_perte_man"/>
    <field editable="0" name="scenario_perte_mercicor"/>
    <field editable="0" name="scenario_perte_pmi"/>
    <field editable="1" name="score_mercicor"/>
    <field editable="1" name="station_man"/>
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
        <Option type="QString" name="nm-rel" value=""/>
      </config>
    </widget>
    <widget name="pression_habitat_pression_etat_ecologique-pression">
      <config type="Map">
        <Option type="QString" name="nm-rel" value=""/>
      </config>
    </widget>
  </widgets>
  <layerGeometryType>2</layerGeometryType>
</qgis>
