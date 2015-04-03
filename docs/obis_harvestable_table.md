# harvestable
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_harvestable |
|ron_id|integer|[fk_harvestable_ron](obis_rons_table) |
|harvestable_type_id|integer||
|url|character varying||
|description|character varying||
|active|boolean||
