# dist_sp_01deg
database: [obis](../)  
schema: [portal](portal)  

    SELECT cs6m_valids.cscode, cs6m_valids.valid_id, cs6m_valids.nexcl, cs6m_valids.nincl, cs6m_valids.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name FROM (summaries.cs6m_valids JOIN portal.species_summary ON ((cs6m_valids.valid_id = species_summary.valid_id)));