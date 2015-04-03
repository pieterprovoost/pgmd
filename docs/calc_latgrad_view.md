# latgrad
database: [obis](../)  
schema: [calc](calc)  

    SELECT (regexp_replace(st_astext(st_centroid(map6m.geom)), '^[^(]*[(][^ ]* ([^)]*)[)]$'::text, '\\1'::text))::real AS lat, count(*) AS nsquares, sum(map6m.n) AS nrecords FROM calc.map6m GROUP BY regexp_replace(st_astext(st_centroid(map6m.geom)), '^[^(]*[(][^ ]* ([^)]*)[)]$'::text, '\\1'::text) ORDER BY (regexp_replace(st_astext(st_centroid(map6m.geom)), '^[^(]*[(][^ ]* ([^)]*)[)]$'::text, '\\1'::text))::real;