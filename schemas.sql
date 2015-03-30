select distinct(t.table_schema)
from information_schema.tables t
where t.table_schema not in %s
order by t.table_schema;
