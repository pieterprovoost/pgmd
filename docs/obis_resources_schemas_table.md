# resources_schemas
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|resource_id|integer|[fk_resources_schemas_resource](obis_resources_table) pk_resources_schemas |
|schema_id|integer|[fk_resources_schemas_schema](obis_schemas_table) pk_resources_schemas |
