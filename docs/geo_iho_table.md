# iho
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|seas_pkey |
|seaname|character varying||
|seacode|character varying||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
