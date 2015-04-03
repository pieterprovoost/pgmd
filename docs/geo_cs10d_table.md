# cs10d
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|geom|USER-DEFINED|enforce_dims_the_geom enforce_geotype_the_geom enforce_srid_the_geom |
|id|integer|pk_cs10d |
|cscode|character|uc_cscode_cs10d |
|landlocked|boolean||
