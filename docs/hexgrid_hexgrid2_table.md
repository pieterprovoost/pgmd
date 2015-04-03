# hexgrid2
database: [obis](../)  
schema: [hexgrid](hexgrid)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_hexgrid2 |
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
|centrelat|double precision||
|centrelon|double precision||
|area|double precision||