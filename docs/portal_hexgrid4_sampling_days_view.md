# hexgrid4_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.hexgrid4_id, c.number_of_days_visited, c.min_date, c.max_date, g.geom FROM (calc.hexgrid4_sampling_days c JOIN hexgrid.hexgrid4 g ON ((g.id = c.hexgrid4_id)));