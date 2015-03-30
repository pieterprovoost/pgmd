SELECT c.table_schema, c.table_name, c.column_name, c.ordinal_position, c.is_nullable, c.data_type
FROM information_schema.columns c
where c.table_schema not in %s
order by c.table_schema, c.table_name, c.ordinal_position;
