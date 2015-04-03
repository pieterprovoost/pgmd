# dist_sp_res_1deg
database: [obis](../)  
schema: [portal](portal)  

    SELECT cs1d_res_valids.cscode, cs1d_res_valids.valid_id, cs1d_res_valids.nexcl, cs1d_res_valids.nincl, cs1d_res_valids.resource_id, cs1d_res_valids.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name, resources.resname FROM ((summaries.cs1d_res_valids JOIN portal.species_summary ON ((cs1d_res_valids.valid_id = species_summary.valid_id))) JOIN obis.resources ON ((cs1d_res_valids.resource_id = resources.id)));