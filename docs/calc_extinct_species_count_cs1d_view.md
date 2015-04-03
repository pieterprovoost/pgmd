# extinct_species_count_cs1d
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_cs1d.cscode, count(extinct_species_recordcount_cs1d.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_cs1d GROUP BY extinct_species_recordcount_cs1d.cscode;