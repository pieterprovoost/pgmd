select v.schemaname, v.viewname, v.definition
from pg_catalog.pg_views v
where v.schemaname not in %s
order by v.schemaname, v.viewname;
