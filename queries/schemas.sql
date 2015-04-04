select n.nspname
from pg_catalog.pg_namespace n
where n.nspname not in %s
and n.nspname not like '%%_temp_%%'
order by n.nspname;
