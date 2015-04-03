# cs6m
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_cs6m |
|cscode|character varying|uc_cscode_cs6m |
|geom|USER-DEFINED|enforce_dims_the_geom enforce_geotype_the_geom enforce_srid_the_geom |
