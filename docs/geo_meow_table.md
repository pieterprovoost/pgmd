# meow
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|meow_pkey |
|eco_code|integer||
|ecoregion|character varying||
|prov_code|integer||
|province|character varying||
|rlm_code|integer||
|realm|character varying||
|alt_code|integer||
|eco_code_x|integer||
|lat_zone|character varying||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
