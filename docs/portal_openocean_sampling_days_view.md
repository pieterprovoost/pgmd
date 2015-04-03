# openocean_sampling_days
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.number_of_days_visited, c.min_date, c.max_date FROM calc.openocean_sampling_days c;