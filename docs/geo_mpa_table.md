# mpa
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|mpa_pkey |
|wdpaid|numeric||
|objectid|numeric||
|wdpa_pid|numeric||
|country|character varying||
|sub_loc|character varying||
|name|character varying||
|orig_name|character varying||
|desig|character varying||
|desig_eng|character varying||
|desig_type|character varying||
|iucn_cat|character varying||
|marine|smallint||
|rep_m_area|numeric||
|rep_area|numeric||
|status|character varying||
|status_yr|numeric||
|gov_type|character varying||
|mang_auth|character varying||
|int_crit|character varying||
|mang_plan|character varying||
|official|smallint||
|is_point|smallint||
|no_take|character varying||
|no_tk_area|numeric||
|metadata_i|numeric||
|action|character varying||
|geom|USER-DEFINED|enforce_dims_geom enforce_geotype_geom enforce_srid_geom |
