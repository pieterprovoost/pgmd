# rons_actors
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|ron_id|integer|[fk_rons_actors_ron](obis_rons_table) pk_rons_actors |
|actor_id|integer|[fk_ron_actor](obis_actors_table) pk_rons_actors |
|role_id|integer|[fk_role](obis_roles_table) |
