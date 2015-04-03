# cs2d_valids
database: [obis](../)  
schema: [summaries](summaries)  

|Column|Type|Constraint|
|:---|:---|:---|
|cscode|character varying|pk_cs2d_valids |
|valid_id|integer|pk_cs2d_valids |
|nexcl|integer||
|nincl|integer||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
