# hexgrid2_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.hexgrid2_id, c.number_of_days_visited, c.min_date, c.max_date, g.geom FROM (calc.hexgrid2_sampling_days c JOIN hexgrid.hexgrid2 g ON ((g.id = c.hexgrid2_id)));