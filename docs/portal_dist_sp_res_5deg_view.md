# dist_sp_res_5deg
database: [obis](../)  
schema: [portal](portal)  

    SELECT cs5d_res_valids.cscode, cs5d_res_valids.valid_id, cs5d_res_valids.nexcl, cs5d_res_valids.nincl, cs5d_res_valids.resource_id, cs5d_res_valids.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name, resources.resname FROM ((summaries.cs5d_res_valids JOIN portal.species_summary ON ((cs5d_res_valids.valid_id = species_summary.valid_id))) JOIN obis.resources ON ((cs5d_res_valids.resource_id = resources.id)));