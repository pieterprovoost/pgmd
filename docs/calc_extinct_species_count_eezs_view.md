# extinct_species_count_eezs
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_eezs.geom_id, count(extinct_species_recordcount_eezs.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_eezs GROUP BY extinct_species_recordcount_eezs.geom_id;