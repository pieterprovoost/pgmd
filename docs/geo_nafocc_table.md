# nafocc
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|dateobserved|date||
|lon|double precision||
|lat|double precision||
|code|character varying||
|myst|real||
|nafo_zone|character varying||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
|id|integer|pk_nafocc |
