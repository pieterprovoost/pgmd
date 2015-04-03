# dist_sp_lme
database: [obis](../)  
schema: [portal](portal)  

    SELECT h.id, h.valid_id, h.nexcl, h.nincl, g.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name FROM ((summaries.lme_valids h JOIN geo.lme g ON ((h.id = g.id))) JOIN portal.species_summary ON ((h.valid_id = species_summary.valid_id)));