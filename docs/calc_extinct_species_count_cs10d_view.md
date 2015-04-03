# extinct_species_count_cs10d
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_cs10d.cscode, count(extinct_species_recordcount_cs10d.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_cs10d GROUP BY extinct_species_recordcount_cs10d.cscode;