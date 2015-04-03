# drs
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|bigint|pk_drs |
|resource_id|integer|[fk_resource](obis_resources_table) |
|sname_id|integer|[fk_sname](obis_snames_table) |
|lifestage|character varying||
|datelastcached|timestamp without time zone||
|basisofrecord|character varying||
|latitude|double precision||
|longitude|double precision||
|coordinateprecision|real||
|datecollected|timestamp with time zone||
|dateprecision|interval||
|depth|real||
|depthprecision|real||
|temperature|real||
|position_id|integer||
|display|character varying||
|valid_id|integer|[fk_tnames_valid](obis_tnames_table) |
|datelastmodified|character varying||
|qc|bigint||
