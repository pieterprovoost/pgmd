# lme_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.lme_id, c.number_of_days_visited, c.min_date, c.max_date, g.geom FROM (calc.lme_sampling_days c JOIN geo.lme g ON ((g.id = c.lme_id)));