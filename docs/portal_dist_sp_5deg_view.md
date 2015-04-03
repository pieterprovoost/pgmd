# dist_sp_5deg
database: [obis](../)  
schema: [portal](portal)  

    SELECT cs5d_valids.cscode, cs5d_valids.valid_id, cs5d_valids.nexcl, cs5d_valids.nincl, cs5d_valids.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name FROM (summaries.cs5d_valids JOIN portal.species_summary ON ((cs5d_valids.valid_id = species_summary.valid_id)));