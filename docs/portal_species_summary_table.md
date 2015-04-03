# species_summary
database: [obis](../)  
schema: [portal](portal)  

|Column|Type|Constraint|
|:---|:---|:---|
|tname_id|integer|pk_species_summary |
|valid_id|integer||
|scientific|character varying||
|authority|character varying||
|parent_valid_id|integer||
|rank_id|smallint||
|rank_name|character varying||
|kingdom_id|integer||
|num_records|bigint||
|num_records_incl|bigint||
|num_resources|bigint||
|date_min|timestamp without time zone||
|date_max|timestamp without time zone||
|data_extent|USER-DEFINED||
|depth_min|real||
|depth_max|real||
|bottomdepth_min|integer||
|bottomdepth_max|integer||
|woa_depth_min|integer||
|woa_depth_max|integer||
|temperature_min|real||
|temperature_max|real||
|salinity_min|real||
|salinity_max|real||
|nitrate_min|real||
|nitrate_max|real||
|oxygen_min|real||
|oxygen_max|real||
|phosphate_min|real||
|phosphate_max|real||
|silicate_min|real||
|silicate_max|real||
|worms_id|integer||
|storedpath|character varying||
