# extinct_species_count_cs6m
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_cs6m.cscode, count(extinct_species_recordcount_cs6m.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_cs6m GROUP BY extinct_species_recordcount_cs6m.cscode;