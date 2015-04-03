# v_redlist_for_gef_twap_oo
database: [obis](../)  
schema: [iucn2014](iucn2014)  

    SELECT v_redlist.iucn_species_id, v_redlist.iucn_scientific_name, v_redlist.match_type, v_redlist.aphiaid_accepted, v_redlist.scientificname, v_redlist.scientificname_accepted, v_redlist.ismarine, v_redlist.red_list_status, v_redlist.tname_id, v_redlist.tname, v_redlist.tauthor FROM iucn2014.v_redlist WHERE ((v_redlist.tname_id IS NOT NULL) AND ((v_redlist.red_list_status)::text = ANY (ARRAY[('EN'::character varying)::text, ('CR'::character varying)::text, ('VU'::character varying)::text])));