# hexgrid3_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.hexgrid3_id, c.number_of_days_visited, c.min_date, c.max_date, g.geom FROM (calc.hexgrid3_sampling_days c JOIN hexgrid.hexgrid3 g ON ((g.id = c.hexgrid3_id)));