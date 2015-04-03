# harvest_to_edc_field_mapping
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_harvest_to_obis_field_mapping |
|temp_table_column_name|character varying||
|temp_table_data_type|character varying||
|edc_column_name|character varying||
|edc_data_type|character varying||
|harvestable_type_id|integer|[fk_harvest_to_edc_field_mapping_harvestable_type](obis_harvestable_type_table) |
|active|boolean||
