select t.tgname, n.nspname, c.relname, n.nspname, p.proname, a.nspname, o.conname,
	case t.tgtype & cast(2 as int2)
		when 0 then 'after'
		else 'before'
	end as trigger_type,
	case t.tgtype & cast(28 as int2)
		when 16 then array['update']
		when  8 then array['delete']
		when  4 then array['insert']
		when 20 then array['insert', 'update']
		when 28 then array['insert', 'update', 'delete']
		when 24 then array['update', 'delete']
		when 12 then array['insert', 'delete']
	end as trigger_event,
	case t.tgtype & cast(1 as int2)
		when 0 then 'statement'
		else 'row'
	end as action_orientation
from pg_catalog.pg_trigger t
left join pg_catalog.pg_class c
on t.tgrelid = c.oid
left join pg_catalog.pg_proc p
on t.tgfoid = p.oid
left join pg_catalog.pg_namespace m
on p.pronamespace = m.oid
left join pg_catalog.pg_namespace n
on c.relnamespace = n.oid
left join pg_catalog.pg_constraint o
on t.tgconstraint = o.oid
left join pg_catalog.pg_namespace a
on o.connamespace = a.oid
where n.nspname not in %s
order by n.nspname, c.relname, t.tgname;
