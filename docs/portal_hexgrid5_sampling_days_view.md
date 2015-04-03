# hexgrid5_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.hexgrid5_id, c.number_of_days_visited, c.min_date, c.max_date, g.geom FROM (calc.hexgrid5_sampling_days c JOIN hexgrid.hexgrid5 g ON ((g.id = c.hexgrid5_id)));