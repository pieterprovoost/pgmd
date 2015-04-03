# tnames
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_cleannames |
|tname|character varying||
|tauthor|character varying||
|valid_id|integer|[fk_tnames_valid_id](obis_tnames_table) [fk_valid](obis_tnames_table) |
|display|character||
|displayremark|text||
|rank_id|smallint||
|parent_id|integer|[fk_parent](obis_tnames_table) |
|storedpath|character varying||
|worms_id|integer||
|col_id|integer||
|irmng_id|integer||
|itis_id|integer||
|date_worms_last_checked|timestamp without time zone||
|worms_id_mismatch|boolean||
|number_of_worms_matches_on_tname|integer||
|worms_match_type|character varying||
