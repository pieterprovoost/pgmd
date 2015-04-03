# oceanseas
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|gid|integer|oceanseas_pkey |
|name|character varying||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
