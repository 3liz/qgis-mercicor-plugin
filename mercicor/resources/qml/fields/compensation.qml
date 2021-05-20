<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.10.14-A Coruña" styleCategories="Fields">
  <fieldConfiguration>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="nom">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="scenario_id">
      <editWidget type="RelationReference">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowAddFeatures" value="false"/>
            <Option type="bool" name="AllowNULL" value="false"/>
            <Option type="bool" name="MapIdentification" value="false"/>
            <Option type="bool" name="OrderByValue" value="false"/>
            <Option type="bool" name="ReadOnly" value="false"/>
            <Option type="QString" name="Relation" value="scenario_compensation-compensation"/>
            <Option type="bool" name="ShowForm" value="false"/>
            <Option type="bool" name="ShowOpenFormButton" value="true"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="coeff_risque">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowNull" value="true"/>
            <Option type="double" name="Max" value="3"/>
            <Option type="double" name="Min" value="1"/>
            <Option type="int" name="Precision" value="0"/>
            <Option type="double" name="Step" value="1"/>
            <Option type="QString" name="Style" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="coeff_delais">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowNull" value="true"/>
            <Option type="double" name="Max" value="4"/>
            <Option type="double" name="Min" value="1"/>
            <Option type="int" name="Precision" value="0"/>
            <Option type="double" name="Step" value="1"/>
            <Option type="QString" name="Style" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="id" index="0"/>
    <alias name="" field="nom" index="1"/>
    <alias name="" field="scenario_id" index="2"/>
    <alias name="" field="coeff_risque" index="3"/>
    <alias name="" field="coeff_delais" index="4"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" field="id" applyOnUpdate="0"/>
    <default expression="" field="nom" applyOnUpdate="0"/>
    <default expression="" field="scenario_id" applyOnUpdate="0"/>
    <default expression="" field="coeff_risque" applyOnUpdate="0"/>
    <default expression="" field="coeff_delais" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" field="id" unique_strength="1" constraints="3" notnull_strength="1"/>
    <constraint exp_strength="0" field="nom" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="scenario_id" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="coeff_risque" unique_strength="0" constraints="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="coeff_delais" unique_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" exp="" desc=""/>
    <constraint field="nom" exp="" desc=""/>
    <constraint field="scenario_id" exp="" desc=""/>
    <constraint field="coeff_risque" exp="" desc=""/>
    <constraint field="coeff_delais" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <layerGeometryType>2</layerGeometryType>
</qgis>
