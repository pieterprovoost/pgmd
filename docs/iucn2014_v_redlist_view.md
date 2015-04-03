# v_redlist
database: [obis](../)  
schema: [iucn2014](iucn2014)  

    SELECT m.iucn_species_id, r.scientific_name AS iucn_scientific_name, m.match_type, m.aphiaid_accepted, m.scientificname, m.scientificname_accepted, m.ismarine, r.red_list_status, t.id AS tname_id, t.tname, t.tauthor FROM ((iucn2014.redlist r JOIN iucn2014.redlist_matched m ON ((r.species_id = m.iucn_species_id))) LEFT JOIN obis.tnames t ON ((m.aphiaid_accepted = t.worms_id))) WHERE (m.aphiaid_accepted IS NOT NULL);