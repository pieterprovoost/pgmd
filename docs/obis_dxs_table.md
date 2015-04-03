# dxs
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|dr_id|bigint|pk_dxs |
|resource_id|integer||
|sname_id|integer||
|datelastmodified|character varying||
|recordlastcached|character varying||
|sourceofrecord|text||
|citation|text||
|recordurl|character varying||
|basisofrecord|character varying||
|institutioncode|character varying||
|collectioncode|character varying||
|catalognumber|character varying||
|collector|character varying||
|yearcollected|character varying||
|startyearcollected|character varying||
|endyearcollected|character varying||
|monthcollected|character varying||
|startmonthcollected|character varying||
|endmonthcollected|character varying||
|daycollected|character varying||
|startdaycollected|character varying||
|enddaycollected|character varying||
|starttimecollected|timestamp without time zone||
|endtimecollected|timestamp without time zone||
|julianday|integer||
|startjulianday|integer||
|endjulianday|integer||
|timeofday|real||
|starttimeofday|real||
|endtimeofday|real||
|timezone|character varying||
|locality|text||
|ocean|character varying||
|country|character varying||
|state|character varying||
|county|character varying||
|latitude|double precision||
|longitude|double precision||
|coordinateprecision|real||
|cscode|character||
|slatitude|double precision||
|elatitude|double precision||
|slongitude|double precision||
|elongitude|double precision||
|seprecision|real||
|depth|real||
|depthprecision|real||
|minimumdepth|real||
|maximumdepth|real||
|depthrange|character varying||
|datecollected|timestamp without time zone||
|lifestage|character varying||
|identifiedby|character varying||
|yearidentified|character varying||
|monthidentified|character varying||
|dayidentified|character varying||
|typestatus|character varying||
|collectornumber|character varying||
|fieldnumber|character varying||
|temperature|real||
|sex|character varying||
|preparationtype|character varying||
|individualcount|real||
|observedindividualcount|real||
|observedweight|real||
|samplesize|character varying||
|previouscatalognumber|character varying||
|relationshiptype|character varying||
|relatedcatalogitem|character varying||
|notes|text||
|concatenated|character varying||
|scientificnameid|character varying||
