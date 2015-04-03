# parse_decimal_time
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE temp_time TEXT;
    DECLARE _hours TEXT;
    DECLARE _time_in text;
    DECLARE _remainder DOUBLE PRECISION;
    DECLARE _minutes INT;
    DECLARE _seconds INT;
    DECLARE time2 TEXT;
    DECLARE starttime TEXT;
    DECLARE endtime TEXT;
    DECLARE r time without time zone;
    DECLARE twtz_time2 time without time zone;
    DECLARE temp_t_time character varying(100);
    BEGIN
    	r := null;
    
    	_time_in := trim(regexp_replace(time_in, E' \+00:00$', ''));
    	_time_in := trim(regexp_replace(time_in, E' 00:00$', ''));
    	
    	-- if we have a time with a decimal point
    	if (strpos(_time_in, '.') > 0) then
    
    		_hours := substr(_time_in, 1, strpos(_time_in, '.') - 1);
    		_remainder := ('0.' || substr(_time_in, strpos(_time_in, '.') + 1))::double precision;
    		
    		--raise notice 'remainder =  %', _remainder;
    
    		_minutes = round(_remainder * 60);
    		--raise notice 'minutes =  %', _minutes;
    		
    		_seconds = round(((_remainder * 60) - _minutes) * 60);
    
    		if (_seconds < 0) then
    			_seconds := 0;
    		end if;
    		
    		--raise notice 'seconds =  %', _seconds;
    		
    		r := (lpad(_hours, 2, '0') || ':' || lpad(_minutes::text,2,'0') || ':' || lpad(_seconds::text, 2, '0'))::time without time zone;
    
            -- we only have a whole number
    	else
    		r = (lpad( ((_time_in::int)::text),2,'0') || ':00:00')::time without time zone;
    	end if;
    	
    	RETURN r;
    	
    exception
        when invalid_text_representation then
            return null;
    END;
