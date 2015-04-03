# dist_sp_hexgrid4
database: [obis](../)  
schema: [portal](portal)  

    SELECT h.hex_id AS id, h.valid_id, h.nexcl, h.nincl, g.geom, species_summary.scientific, species_summary.authority, species_summary.rank_name FROM ((hexgrid.summ_hexgrid4_valids h JOIN hexgrid.hexgrid4 g ON ((h.hex_id = g.id))) JOIN portal.species_summary ON ((h.valid_id = species_summary.valid_id)));