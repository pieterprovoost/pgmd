# hexgrid1_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.hexgrid1_id, c.number_of_days_visited, c.min_date, c.max_date, g.geom FROM (calc.hexgrid1_sampling_days c JOIN hexgrid.hexgrid1 g ON ((g.id = c.hexgrid1_id)));