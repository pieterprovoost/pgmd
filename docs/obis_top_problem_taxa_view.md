# top_problem_taxa
database: [obis](../)  
schema: [obis](obis)  

    SELECT regexp_replace((tnames.tname)::text, '^([^ ]+) .*$'::text, '\\1'::text) AS regexp_replace, count(*) AS count FROM obis.tnames WHERE (((tnames.tname)::text ~ ' '::text) AND (tnames.parent_id IS NULL)) GROUP BY regexp_replace((tnames.tname)::text, '^([^ ]+) .*$'::text, '\\1'::text) ORDER BY count(*) DESC;