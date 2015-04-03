# map6m
database: [obis](../)  
schema: [calc](calc)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_map6m |
|cscode|character varying||
|n|integer||
|s|integer||
|shannon|numeric||
|simpson|numeric||
|es|double precision||
|hill_1|numeric||
|hill_2|numeric||
|hill_inf|numeric||
|geom|USER-DEFINED|enforce_dims_the_geom enforce_geotype_the_geom enforce_srid_the_geom |
