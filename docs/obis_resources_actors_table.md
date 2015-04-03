# resources_actors
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|resource_id|integer|pk_resources_actors |
|actor_id|integer|[fk_resource_actor](obis_actors_table) pk_resources_actors |
|role_id|integer|[fk_resources_actors_role](obis_roles_table) |
