# lme66
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|lme66_pkey |
|objectid|integer||
|lme_number|numeric||
|lme_name|character varying||
|shape_leng|numeric||
|shape_area|numeric||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
