# fips_country
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|gid|integer|fips_country_pkey |
|fips_cntry|character varying||
|cntry_name|character varying||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
