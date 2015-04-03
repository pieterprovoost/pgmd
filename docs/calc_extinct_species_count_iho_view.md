# extinct_species_count_iho
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_iho.geom_id, count(extinct_species_recordcount_iho.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_iho GROUP BY extinct_species_recordcount_iho.geom_id;