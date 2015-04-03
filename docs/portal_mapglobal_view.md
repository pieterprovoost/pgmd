# mapglobal
database: [obis](../)  
schema: [portal](portal)  

    SELECT c.n, c.s, p.s AS number_of_phyla, (c.shannon)::real AS shannon, (c.simpson)::real AS simpson, (c.es)::real AS es, c.hill_1, c.hill_2, c.hill_inf AS hill_infinite, s.number_of_days_visited AS number_of_1day_sampling_events, s.min_date AS date_of_earliest_record, s.max_date AS date_of_latest_record FROM ((calc.mapglobal c LEFT JOIN calc.mapglobal_30_phylum p ON ((1 = 1))) LEFT JOIN calc.global_sampling_days s ON ((1 = 1)));