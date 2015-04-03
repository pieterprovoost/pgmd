# cntry98
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|gid|integer|cntry98_pkey |
|fips_cntry|character varying||
|gmi_cntry|character varying||
|iso_2digit|character varying||
|iso_3digit|character varying||
|cntry_name|character varying||
|sovereign|character varying||
|pop_cntry|bigint||
|sqkm_cntry|double precision||
|sqmi_cntry|double precision||
|curr_type|character varying||
|curr_code|character varying||
|landlocked|character varying||
|color_map|character varying||
|dist_1|double precision||
|name_1|character varying||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
