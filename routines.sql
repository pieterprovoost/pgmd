select r.routine_schema, r.routine_name, r.external_language, r.routine_body, r.routine_definition
from information_schema.routines r
where specific_schema not in ('pg_catalog', 'information_schema')
order by r.routine_schema, r.routine_name;
