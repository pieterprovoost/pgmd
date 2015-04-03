# cs2d
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|cscode|character varying|uc_cscode_cs2d |
|geom|USER-DEFINED|enforce_dims_the_geom enforce_geotype_the_geom enforce_srid_the_geom |
|id|integer|pk_cs2d |
