# mf_clean_sauthor_recursively
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE
       new_sauthor varchar(200);
       bMatched boolean;
       i int;
    BEGIN
       --i := 1;
       bMatched := true;
       new_sauthor := sauthor;
       while (bMatched = true) LOOP
    	select cleaned_sauthor, matched from obis.mf_clean_sauthor(new_sauthor) into new_sauthor, bMatched;
    	--raise notice 'iterations = %', i;
    	--raise notice 'new_sname = %', new_sname;
    	--raise notice 'bMatched = %', bMatched;
    	--i:=i+1;
       END LOOP;
    
       return new_sauthor;
    END;
