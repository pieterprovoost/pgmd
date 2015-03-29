select t.table_schema, t.table_name, t.table_type
from information_schema.tables t
where t.table_schema not in ('pg_catalog', 'information_schema')
and t.table_type = 'BASE TABLE'
order by t.table_schema, t.table_name;