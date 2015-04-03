# lme66_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.lme66_id, c.number_of_days_visited, c.min_date, c.max_date, g.geom FROM (calc.lme66_sampling_days c JOIN geo.lme66 g ON ((g.id = c.lme66_id)));