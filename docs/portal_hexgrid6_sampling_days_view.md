# hexgrid6_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.hexgrid6_id, c.number_of_days_visited, c.min_date, c.max_date, g.geom FROM (calc.hexgrid6_sampling_days c JOIN hexgrid.hexgrid6 g ON ((g.id = c.hexgrid6_id)));