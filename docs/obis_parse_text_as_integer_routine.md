# parse_text_as_integer
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE _time_in text;
    BEGIN
    	_time_in := trim(regexp_replace(text_in, E' \+00:00$', ''));
    	_time_in := trim(regexp_replace(text_in, E' 00:00$', ''));
    	RETURN _time_in::real::integer;
    	
    exception
        when invalid_text_representation then
            return null;
    END;
