# extinct_species_count_lme66
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_lme66.geom_id, count(extinct_species_recordcount_lme66.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_lme66 GROUP BY extinct_species_recordcount_lme66.geom_id;