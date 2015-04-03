# snames
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_snames |
|sname|character varying||
|sauthor|character varying||
|tname|character varying||
|tauthor|character varying||
|lifestage|character varying||
|accuracy|character varying||
|remark|character varying||
|concatenated|character varying||
|tname_id|integer|[fk_tnames](obis_tnames_table) |
