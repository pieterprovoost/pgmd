# cnames
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_comnames |
|tname_id|integer|[fk_taxon](obis_tnames_table) |
|lifestage|character varying||
|cname|character varying||
|language_id|integer|[fk_language](obis_languages_table) |
|preferredflag|boolean||
|source_id|integer||
|notes|text||
