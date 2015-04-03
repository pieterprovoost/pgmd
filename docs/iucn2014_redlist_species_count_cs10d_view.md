# redlist_species_count_cs10d
database: [obis](../)  
schema: [iucn2014](iucn2014)  

    WITH t1 AS (SELECT DISTINCT s.cscode, s.valid_id FROM (summaries.cs10d_valids s JOIN iucn2014.v_redlist_for_gef_twap_oo r ON ((s.valid_id = r.tname_id)))) SELECT t1.cscode, count(*) AS redlist_species_count FROM t1 GROUP BY t1.cscode;