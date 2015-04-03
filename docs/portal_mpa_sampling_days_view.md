# mpa_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.mpa_id, c.number_of_days_visited, c.min_date, c.max_date, g.geom FROM (calc.mpa_sampling_days c JOIN geo.mpa g ON ((g.id = c.mpa_id)));