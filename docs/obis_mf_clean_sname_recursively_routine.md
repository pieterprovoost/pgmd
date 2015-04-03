# mf_clean_sname_recursively
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE
       new_sname varchar(200);
       bMatched boolean;
       i int;
    BEGIN
       --i := 1;
       bMatched := true;
       new_sname := sname;
       while (bMatched = true) LOOP
    	select cleaned_sname, matched from obis.mf_clean_sname(new_sname) into new_sname, bMatched;
    	--raise notice 'iterations = %', i;
    	--raise notice 'new_sname = %', new_sname;
    	--raise notice 'bMatched = %', bMatched;
    	--i:=i+1;
       END LOOP;
    
       return new_sname;
    END;
