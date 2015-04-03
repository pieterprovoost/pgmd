# dist_sp_res_01deg
database: [obis](../)  
schema: [portal](portal)  

    SELECT cs6m_res_valids.cscode, cs6m_res_valids.valid_id, cs6m_res_valids.nexcl, cs6m_res_valids.nincl, cs6m_res_valids.resource_id, cs6m_res_valids.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name, resources.resname FROM ((summaries.cs6m_res_valids JOIN portal.species_summary ON ((cs6m_res_valids.valid_id = species_summary.valid_id))) JOIN obis.resources ON ((cs6m_res_valids.resource_id = resources.id)));