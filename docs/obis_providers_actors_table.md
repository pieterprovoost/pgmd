# providers_actors
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|provider_id|integer|[fk_provider_actor](obis_providers_table) pk_providers_actors |
|actor_id|integer|[fk_providers_actors](obis_actors_table) pk_providers_actors |
|role_id|integer|[fk_providers_actors_role](obis_roles_table) |
