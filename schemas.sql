select distinct(t.table_schema)
from information_schema.tables t
where t.table_schema not in ('pg_catalog', 'information_schema')
order by t.table_schema;