# dist_sp_res_hexgrid6
database: [obis](../)  
schema: [portal](portal)  

    SELECT h.hex_id AS id, h.valid_id, h.nexcl, h.nincl, h.resource_id, g.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name, resources.resname FROM (((hexgrid.summ_hexgrid6_res_valids h JOIN hexgrid.hexgrid6 g ON ((h.hex_id = g.id))) JOIN portal.species_summary ON ((h.valid_id = species_summary.valid_id))) JOIN obis.resources ON ((h.resource_id = resources.id)));