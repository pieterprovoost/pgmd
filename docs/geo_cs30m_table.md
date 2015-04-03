# cs30m
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_cs30m |
|cscode|character varying|uc_cscode_cs30m |
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_the_geom enforce_srid_geom |
|landlocked|boolean||
