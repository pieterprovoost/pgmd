# extinct_species_count_mpa
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_mpa.geom_id, count(extinct_species_recordcount_mpa.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_mpa GROUP BY extinct_species_recordcount_mpa.geom_id;