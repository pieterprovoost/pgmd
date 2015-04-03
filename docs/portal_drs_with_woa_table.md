# drs_with_woa
database: [obis](../)  
schema: [portal](portal)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_drs_with_woa |
|resource_id|integer||
|resname|character varying||
|lifestage|character varying||
|basisofrecord|character varying||
|latitude|double precision||
|longitude|double precision||
|coordinateprecision|real||
|datelastcached|timestamp without time zone||
|datecollected|timestamp with time zone||
|dateprecision|character varying||
|datelastmodified|character varying||
|yearcollected|integer||
|monthcollected|integer||
|daycollected|integer||
|valid_id|integer||
|sname|character varying||
|sauthor|character varying||
|tname|character varying||
|tauthor|character varying||
|storedpath|character varying||
|geom|USER-DEFINED||
|cs6m|character varying||
|eez_id|integer||
|lme_id|integer||
|meow_id|integer||
|iho_id|integer||
|fao_id|integer||
|mwhs_id|integer||
|depth|real||
|depthprecision|real||
|bottomdepth|integer||
|display|character varying||
|woa_depth|integer||
|temperature|real||
|salinity|real||
|nitrate|real||
|oxygen|real||
|phosphate|real||
|silicate|real||
