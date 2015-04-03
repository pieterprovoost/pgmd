# dist_sp_05deg
database: [obis](../)  
schema: [portal](portal)  

    SELECT cs30m_valids.cscode, cs30m_valids.valid_id, cs30m_valids.nexcl, cs30m_valids.nincl, cs30m_valids.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name FROM (summaries.cs30m_valids JOIN portal.species_summary ON ((cs30m_valids.valid_id = species_summary.valid_id)));