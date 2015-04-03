# fprojects_actors
database: [obis](../)  
schema: [obis](obis)  

|Column|Type|Constraint|
|:---|:---|:---|
|fproject_id|integer|pk_fproject_actors |
|actor_id|integer|[fk_fprojects_actors](obis_actors_table) pk_fproject_actors |
|role_id|integer|[fk_fprojects_actors_role](obis_roles_table) |
