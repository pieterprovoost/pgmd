# mwhs
database: [obis](../)  
schema: [geo](geo)  

|Column|Type|Constraint|
|:---|:---|:---|
|ogc_fid|integer|mwhs_pk |
|wkb_geometry|USER-DEFINED|enforce_dims_wkb_geometry enforce_geotype_wkb_geometry enforce_srid_wkb_geometry |
|refid|integer||
|refid2|integer||
|country|character varying||
|mrgi|integer||
|year|integer||
|site_name|character varying||
