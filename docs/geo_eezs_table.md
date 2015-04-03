# eezs
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|gid|integer|eezs_pkey |
|eez|character varying||
|country|character varying||
|id|smallint||
|sovereign|character varying||
|remarks|character varying||
|sov_id|smallint||
|iso_3digit|character varying||
|gazid|numeric||
|area_km2|numeric||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
