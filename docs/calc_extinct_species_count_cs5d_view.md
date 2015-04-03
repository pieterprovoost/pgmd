# extinct_species_count_cs5d
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_cs5d.cscode, count(extinct_species_recordcount_cs5d.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_cs5d GROUP BY extinct_species_recordcount_cs5d.cscode;