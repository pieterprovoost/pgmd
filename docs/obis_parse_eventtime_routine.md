# parse_eventtime
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE returnRecord obis.eventtime;
    DECLARE temp_time TEXT;
    DECLARE time1 TEXT;
    DECLARE time2 TEXT;
    DECLARE starttime TEXT;
    DECLARE endtime TEXT;
    DECLARE twtz_time1 time with time zone;
    DECLARE twtz_time2 time with time zone;
    DECLARE temp_t_time character varying(100);
    BEGIN
    
       returnRecord.timeofday  := null;
       returnRecord.starttimeofday := null;
       returnRecord.endtimeofday := null;
       returnRecord.timezone := null;
       
       if (time_in is not null) then
    
    	temp_time := lower(ltrim(rtrim(time_in)));
    
    	if (temp_time <> '') then
    
    		-- do we have more than 1 time?
    		if (strpos(temp_time, '/') > 0) then
    
    			-- get both dates
    			time1 := ltrim(rtrim(split_part(temp_time, '/', 1)));
    			time2 := ltrim(rtrim(split_part(temp_time, '/', 2)));
    
    			-- if we have a space in the times we do not support the format
    			 if (strpos(time1, ' ') > 0) then
    			    time1 := null;
    			 end if;
    
    			 if (strpos(time2, ' ') > 0) then
    			    time2 := null;
    			 end if;
    
    			  if (time1 is not null and time2 is not null) then
    
    				-- assume decimal hours if the time contains a decimal point or is less than 3 chars in length
    				if ((strpos(time1, '.') > 0) or length (time1) < 3) then
    					twtz_time1 = obis.parse_decimal_time(time1);
    				elsif ( (strpos(time1, ':') > 0) -- contains a :
    				        or (strpos(time1, '+') > 0) -- contains a +
    				        or (strpos(time1, '-') > 0) -- contains a -
    				        or (strpos(time1, 'Z') > 0) -- contains a Z
    				        or (length(time1) > 2) -- contains a Z
    			       ) then
    				        -- parse it into the timeofday;
    					select obis.parse_iso_8601_time(time1) into twtz_time1;
    				end if;
    
    				if ((strpos(time2, '.') > 0) or length (time2) < 3) then
    					twtz_time2 = obis.parse_decimal_time(time2);
    				elsif ( (strpos(time2, ':') > 0) -- contains a :
    				        or (strpos(time2, '+') > 0) -- contains a +
    				        or (strpos(time2, '-') > 0) -- contains a -
    				        or (strpos(time2, 'Z') > 0) -- contains a Z
    				        or (length(time2) > 2) -- contains a Z
    			       ) then
    					select obis.parse_iso_8601_time(time2) into twtz_time2;
    				end if;
    			  
    
    				-- work out which is the earliest
    				if ( twtz_time1 <= twtz_time2) then
    					  starttime:= twtz_time1::text;
    					  endtime := twtz_time2::text;
    				else
    					  starttime := twtz_time2::text;
    					  endtime := twtz_time1::text;
    				end if;
    
    				raise notice 'starttime = %', starttime;
    				raise notice 'endtime = %', endtime;
    
    				-- parse the 2 times into the return fields;
    				select obis.parse_iso_8601_time(starttime)::character varying(100) into returnRecord.starttimeofday;
    				select obis.parse_iso_8601_time(endtime)::character varying(100) into returnRecord.endtimeofday;
    
    				-- I am only going to parse the timezone from the starttime!
    				temp_t_time := obis.parse_iso_8601_time(starttime)::character varying(100);
    
    				if (strpos(temp_t_time, '+') > 0) then
    					select substring(temp_t_time, strpos(temp_t_time, '+'))::character varying(100) into returnRecord.timezone;
    				elsif (strpos(temp_t_time, '-') > 0) then
    					select substring(temp_t_time, strpos(temp_t_time, '-'))::character varying(100) into returnRecord.timezone;
    				end if;
    
    			end if;
    
    		else
    			time1 := temp_time;
    
    			-- assume decimal hours if the time contains a decimal point or is less than 3 chars in length
    			if ((strpos(time1, '.') > 0) or length(time1) < 3) then
    			
    				returnRecord.timeofday = obis.parse_decimal_time(temp_time)::character varying(100);
    				
    			elsif (    (strpos(temp_time, ':') > 0) -- contains a :
    				or (strpos(temp_time, '+') > 0) -- contains a +
    				or (strpos(temp_time, '-') > 0) -- contains a -
    				or (strpos(temp_time, 'Z') > 0) -- contains a Z
    				or (length(temp_time) > 2) -- contains a Z
    			       ) then
    
    					-- parse it into the timeofday;
    					select obis.parse_iso_8601_time(temp_time)::character varying(100) into returnRecord.timeofday;
    					--select (extract (timezone from (obis.parse_iso_8601_time(temp_time)))::interval)::character varying(100) into returnRecord.timezone;
    					temp_t_time := obis.parse_iso_8601_time(temp_time)::character varying(100);
    
    
    					--temp_start_time := obis.parse_iso_8601_time(starttime)::character varying(100);
    
    					if (strpos(temp_t_time, '+') > 0) then
    						select substring(temp_t_time, strpos(temp_t_time, '+'))::character varying(100) into returnRecord.timezone;
    					elsif (strpos(temp_t_time, '-') > 0) then
    						select substring(temp_t_time, strpos(temp_t_time, '-'))::character varying(100) into returnRecord.timezone;
    					end if;
    				
    			end if;
    
    		end if;
    		
    	end if;
    
       end if;
    	
       RETURN returnRecord;
       
    END;
