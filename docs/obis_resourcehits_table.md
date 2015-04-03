# resourcehits
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_resourcehits |
|resource_id|integer|[fk_resources](obis_resources_table) |
|query_id|integer|[fk_query](obis_queries_table) |
|recordcount|integer||
