# iho_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.iho_id, c.number_of_days_visited, c.min_date, c.max_date, g.geom FROM (calc.iho_sampling_days c JOIN geo.iho g ON ((g.id = c.iho_id)));