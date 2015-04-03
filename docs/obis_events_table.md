# events
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_events |
|eventtype_id|integer|[pk_eventtype](obis_eventtypes_table) |
|resource_id|integer|[pk_resource](obis_resources_table) |
|eventdate|date||
|comments|text||
