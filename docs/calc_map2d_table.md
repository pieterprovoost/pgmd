# map2d
database: [obis](../)  
schema: [calc](calc)  

|Column|Type|Constraint|
|:---|:---|:---|
|cscode|text|ix_map2d |
|n|integer||
|s|integer||
|shannon|real||
|simpson|real||
|es|real||
|hill_1|real||
|hill_2|real||
|hill_inf|real||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
