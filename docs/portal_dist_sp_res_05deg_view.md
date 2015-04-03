# dist_sp_res_05deg
database: [obis](../)  
schema: [portal](portal)  

    SELECT cs30m_res_valids.cscode, cs30m_res_valids.valid_id, cs30m_res_valids.nexcl, cs30m_res_valids.nincl, cs30m_res_valids.resource_id, cs30m_res_valids.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name, resources.resname FROM ((summaries.cs30m_res_valids JOIN portal.species_summary ON ((cs30m_res_valids.valid_id = species_summary.valid_id))) JOIN obis.resources ON ((cs30m_res_valids.resource_id = resources.id)));