select t.table_schema, t.table_name, t.table_type
from information_schema.tables t
where t.table_schema not in %s
and t.table_type = 'VIEW'
order by t.table_schema, t.table_name;
