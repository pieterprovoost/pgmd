# fao_complete
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|fao_pkey |
|objectid|integer||
|ocean|character varying||
|subocean|character varying||
|f_area|character varying||
|f_subarea|character varying||
|f_subunit|character varying||
|f_division|character varying||
|f_subdivis|character varying||
|shape_leng|numeric||
|shape_area|numeric||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
