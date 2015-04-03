# dist_sp_1deg
database: [obis](../)  
schema: [portal](portal)  

    SELECT cs1d_valids.cscode, cs1d_valids.valid_id, cs1d_valids.nexcl, cs1d_valids.nincl, cs1d_valids.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name FROM (summaries.cs1d_valids JOIN portal.species_summary ON ((cs1d_valids.valid_id = species_summary.valid_id)));