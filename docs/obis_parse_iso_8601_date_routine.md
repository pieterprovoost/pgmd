# parse_iso_8601_date
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE returnRecord obis.iso_8601_date;
    DECLARE temp_date_in TEXT;
    DECLARE temp_date TEXT;
    DECLARE temp_time TEXT;
    BEGIN
    
       returnRecord._year = null;
       returnRecord._month = null;
       returnRecord._day = null;
       returnRecord._time = null;
       
       if (date_in is not null) then
    
            -- get a trimmed lowercase version of the date with t replaced by a space.
    	temp_date_in = replace(ltrim(rtrim(lower(date_in))), 't', ' '); 
    
            -- we have a space in the date so assume that it is the delimiter between
            -- the date and time parts and split the string based on the position of the space
    	if (strpos(temp_date_in, ' ') > 0) then
    		temp_date := substring(temp_date_in, 0, strpos(temp_date_in, ' '));
    		temp_time := substring(temp_date_in, strpos(temp_date_in, ' ') + 1);
    		
    	-- there is no space so assume we only have a date and no time
    	else
    		temp_date := temp_date_in;
    	end if;
    
    	-- YYYYMMDD              e.g. 20091015     = 15 October 2009
    	-- YYYY-MM-DD            e.g. 2009-10-15   = as above
    	-- YYYYMM                e.g  200910       = NOT ALLOWED BY THE STANDARD
    	-- YYYY-MM               e.g. 2009-10      = October 2009
    	-- YYYY                  e.g. 2009
    	-- YY                    e.g  20           = The century from 2000 to 2099 inclusive
    	
    	-- YYYY-MM-DDThh:mm:ssZ  e.g. 2007-03-01T13:00:00Z
    	-- YYYY-MM-DDThh:mm:ssZ  e.g. 2007-03-01T130000Z
    	-- YYYY-MM-DDThh:mm:ssZ  e.g. 2007-03-01T1300Z
    	-- YYYY-MM-DDThh:mm:ssZ  e.g. 2007-03-01T13:00Z
    	-- YYYY-MM-DDThh:mm:ssZ  e.g. 2007-03-01T13Z
    
    	-- YYYY-MM-DDThh:mm:ssZ  e.g. 2007-03-01 13:00:00Z
    	-- YYYY-MM-DDThh:mm:ssZ  e.g. 2007-03-01 130000Z
    	-- YYYY-MM-DDThh:mm:ssZ  e.g. 2007-03-01 1300Z
    	-- YYYY-MM-DDThh:mm:ssZ  e.g. 2007-03-01 13:00Z
    	-- YYYY-MM-DDThh:mm:ssZ  e.g. 2007-03-01 13Z
    
    	-- YYYY-MM-DDThh:mm:ssZ  e.g. 2007-03-01T13:00:00+2
    
            -- is the date delimited by the '-' character?
    	if (strpos(temp_date, '-') > 0) then
    	
                   returnRecord._year  := lpad(split_part(temp_date, '-', 1), 4, '0');
                   returnRecord._month := lpad(split_part(temp_date, '-', 2), 2, '0');
                   returnRecord._day   := lpad(split_part(temp_date, '-', 3), 2, '0');
    	else 
    
    		if (length(temp_date) >= 4) then
    			returnRecord._year  = substring(temp_date, 1, 4)::integer;
    		end if;
    
    		if (length(temp_date) >= 6) then
    			returnRecord._month  = substring(temp_date, 5, 2)::integer;
    		end if;
    
    		if (length(temp_date) >= 8) then
    			returnRecord._day = substring(temp_date, 7, 2)::integer;
    		end if;
    
    		--if (length(temp_date) > 8) then
    		--	temp_time = lower(ltrim(rtrim(substring(temp_date, 9))));
    		--end if;
    		   
    	end if;
    
    	temp_time := ltrim(rtrim(temp_time));
    
    	if ((temp_time is not null) and (temp_time != '')) then 
    		returnRecord._time = obis.parse_iso_8601_time(temp_time);
    	end if;
    
       end if;
    	
       RETURN returnRecord;
       
    END;
