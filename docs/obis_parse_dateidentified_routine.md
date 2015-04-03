# parse_dateidentified
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE returnRecord obis.dateidentified;
    DECLARE temp_date TEXT;
    BEGIN
    
       returnRecord.yearidentified  := null;
       returnRecord.monthidentified  := null;
       returnRecord.dayidentified := null;
       
       if (date_in <> null) then
    
    	temp_date = ltrim(rtrim(date_in));
    
            -- is the date delimited by "-" characters?
            -- if yes split the date using those characters
    	if (substring(temp_date, 5, 1) = "-") then
               returnRecord.yearidentified  := substring(temp_date, 1, 4)::integer;
    	   returnRecord.monthidentified  := substring(temp_date, 6, 2)::integer;
    	   returnRecord.dayidentified := substring(temp_date, 9, 2)::integer;
    	else
    	   returnRecord.yearidentified  := substring(temp_date, 1, 4)::integer;
    	   returnRecord.monthidentified  := substring(temp_date, 5, 2)::integer;
    	   returnRecord.dayidentified := substring(temp_date, 7, 2)::integer;
    	end if;
    
       end if;
    	
       RETURN returnRecord;
       
    END;
