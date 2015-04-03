# eezlrs
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|eez|character varying||
|country|character varying||
|id|integer|pk_eezs |
|sovereign|character varying||
|remarks|character varying||
|sov_id|integer||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
