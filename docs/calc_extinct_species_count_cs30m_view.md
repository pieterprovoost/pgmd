# extinct_species_count_cs30m
database: [obis](../)  
schema: [calc](calc)  

    SELECT extinct_species_recordcount_cs30m.cscode, count(extinct_species_recordcount_cs30m.valid_id) AS extinct_species_count FROM calc.extinct_species_recordcount_cs30m GROUP BY extinct_species_recordcount_cs30m.cscode;