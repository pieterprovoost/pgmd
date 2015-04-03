# dist_sp_res_iho
database: [obis](../)  
schema: [portal](portal)  

    SELECT h.id, h.valid_id, h.nexcl, h.nincl, h.resource_id, g.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name, resources.resname FROM (((summaries.iho_res_valids h JOIN geo.iho g ON ((h.id = g.id))) JOIN portal.species_summary ON ((h.valid_id = species_summary.valid_id))) JOIN obis.resources ON ((h.resource_id = resources.id)));