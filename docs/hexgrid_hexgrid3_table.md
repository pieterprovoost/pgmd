# hexgrid3
database: [obis](../)  
schema: [hexgrid](hexgrid)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_hexgrid3 |
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
|centrelat|double precision||
|centrelon|double precision||
|area|double precision||
