select n.nspname, r.relname, a.nspname, f.relname, c.conname, c.contype, array_agg(m.ordinal_position::smallint), array_agg(o.ordinal_position::smallint), array_agg(m.column_name::text), array_agg(o.column_name::text)
from pg_catalog.pg_constraint c
-- namespace
left join pg_catalog.pg_namespace n
on c.connamespace = n.oid
-- table
left join pg_catalog.pg_class r
on c.conrelid = r.oid
-- table columns
left join information_schema.columns m
on m.table_schema = n.nspname and m.table_name = r.relname and m.ordinal_position = any(c.conkey)
-- other table
left join pg_catalog.pg_class f
on c.confrelid = f.oid
-- other namespace
left join pg_catalog.pg_namespace a
on f.relnamespace = a.oid
-- other table columns
left join information_schema.columns o
on o.table_schema = n.nspname and o.table_name = r.relname and o.ordinal_position = any(c.confkey)
where n.nspname not in %s
group by n.nspname, r.relname, a.nspname, f.relname, c.conname, c.contype
order by n.nspname, r.relname, a.nspname, f.relname;