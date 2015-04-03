# redlist_species_count_hexgrid4
database: [obis](../)  
schema: [iucn2014](iucn2014)  

    WITH t1 AS (SELECT DISTINCT s.hex_id, s.valid_id FROM (hexgrid.summ_hexgrid4_valids s JOIN iucn2014.v_redlist_for_gef_twap_oo r ON ((s.valid_id = r.tname_id)))) SELECT t1.hex_id, count(*) AS redlist_species_count FROM t1 GROUP BY t1.hex_id;