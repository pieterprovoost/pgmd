# eezs_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.eezs_id, c.number_of_days_visited, c.min_date, c.max_date, g.geom FROM (calc.eezs_sampling_days c JOIN geo.eezs g ON ((g.id = c.eezs_id)));