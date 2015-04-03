# cs5d_res_valids
database: [obis](../)  
schema: [summaries](summaries)  

|Column|Type|Constraint|
|:---|:---|:---|
|cscode|character varying|pk_cs5d_res_valids |
|valid_id|integer|pk_cs5d_res_valids |
|nexcl|integer||
|nincl|integer||
|resource_id|integer|pk_cs5d_res_valids |
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
