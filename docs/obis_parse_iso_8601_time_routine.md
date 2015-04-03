# parse_iso_8601_time
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE returnValue time with time zone;
    DECLARE temp_time TEXT;
    BEGIN
    
       returnValue = null;
    
       if (time_in is not null) then
    
    	temp_time := lower(ltrim(rtrim(time_in)));
    
    	if (temp_time != '') then
    
                    -- remove any prefixing t characters
    		if ( substring(temp_time, 1, 1) = 't' ) then
    			temp_time = substring(temp_time, 2);		
    		end if;
    
    		-- if there are any spaces then the time is not in a good format so return an empty string.
    		if (strpos(temp_time, ' ') > 0) then
    			return null;
    		end if;
    
    		-- if the time string is missing and only contains a time zone.
    		if (strpos(temp_time, '+') = 1) then
    			return null;
    		end if;
    
                    -- if we do not have any : delimiters
    		if (strpos(temp_time, ':') < 1) then
    			if ((length(temp_time) = 1) or (length(temp_time) = 3) or (length(temp_time) = 5)) then
    				temp_time:= '0' || temp_time;
    			end if;
    		end if;
    		
    		returnValue = temp_time::time with time zone;
    
    	end if;
    	
       end if;
    	
       RETURN returnValue;
       
    END;
