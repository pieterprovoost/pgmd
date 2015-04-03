# extinct_species_count_lme
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_lme.geom_id, count(extinct_species_recordcount_lme.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_lme GROUP BY extinct_species_recordcount_lme.geom_id;