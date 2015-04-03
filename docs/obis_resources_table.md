# resources
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_resources |
|resname|character varying||
|resfullname|character varying||
|acronym|character varying||
|digirname|character varying||
|digirurl|character varying||
|abstract|text||
|conceptualschema|character varying||
|website|character varying||
|citation|text||
|usage|text||
|created|text||
|temporalscope|character varying||
|geographicscope|character varying||
|taxonscope|text||
|gcmd_id|character varying||
|ron_id|integer|[fk_ron](obis_rons_table) |
|fproject_id|integer|[fk_fproject](obis_fprojects_table) |
|provider_id|integer|[fk_provider](obis_providers_table) |
|species_cnt|integer||
|taxon_cnt|integer||
|record_cnt|integer||
|imis_dasid|integer||
|date_last_harvested|timestamp without time zone||
