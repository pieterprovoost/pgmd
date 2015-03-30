select n.nspname, p.proname, p.prosrc, p.proargmodes, p.proargnames, l.lanname, t.typname, t.typinput, t.typoutput
from pg_catalog.pg_namespace n
left join pg_catalog.pg_proc p
on n.oid = p.pronamespace
left join pg_catalog.pg_language l
on p.prolang = l.oid
left join pg_catalog.pg_type t
on p.prorettype = t.oid
where n.nspname not in %s;
