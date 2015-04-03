# map01deg_with_geom
database: [obis](../)  
schema: [portal](portal)  

    SELECT g.cscode, g.geom, c.n, c.s, p.s AS number_of_phyla, (c.shannon)::real AS shannon, (c.simpson)::real AS simpson, (c.es)::real AS es, c.hill_1, c.hill_2, c.hill_inf AS hill_infinite, i.redlist_species_count, e.extinct_species_count, s.number_of_days_visited AS number_of_1day_sampling_events, s.min_date AS date_of_earliest_record, s.max_date AS date_of_latest_record FROM (((((geo.cs6m g LEFT JOIN calc.map6m c ON (((c.cscode)::text = (g.cscode)::text))) LEFT JOIN calc.map6m_30_phylum p ON (((p.cscode)::text = (g.cscode)::text))) LEFT JOIN calc.cs6m_sampling_days s ON ((s.cs6m_id = g.id))) LEFT JOIN iucn2014.redlist_species_count_cs6m i ON (((i.cscode)::text = (g.cscode)::text))) LEFT JOIN calc.extinct_species_count_cs6m e ON (((e.cscode)::text = (g.cscode)::text)));